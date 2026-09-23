#!/usr/bin/env python3
"""《The Agency 智能体实战手册》PDF 编译器

将 docs/usage/ 下全部 agent 使用文档按图书结构（封面→版权页→前言→目录→13 个部门分部→终章→编辑手记）
整合为单个 PDF。排版遵循 Book Co-Author 的交付规范：版本化、编辑手记可见、红线贯穿。
"""
import os
import re
import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, NextPageTemplate,
                                HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents

REPO = '/Users/duobinji/Documents/GitHub/agency-agents'
USAGE = os.path.join(REPO, 'docs/usage')
OUT = os.path.join(REPO, 'docs/The-Agency-智能体实战手册.pdf')
BOOK_TITLE = 'The Agency 智能体实战手册'
VERSION = 'V1.0'
DATE = '2026-09-23'
BRANCH = 'docs/agent-usage-guides'

ACCENT = colors.HexColor('#8B5E3C')
INK = colors.HexColor('#1c1917')
BODY_C = colors.HexColor('#2a2620')
MUTE = colors.HexColor('#8a857c')
CODE_BG = colors.HexColor('#f5f4f0')
CODE_BD = colors.HexColor('#e0ddd4')
QUOTE_BG = colors.HexColor('#faf7f2')

PAGE_W, PAGE_H = A4
M_L = M_R = 20 * mm
M_B = 18 * mm
M_T = 18 * mm
AVAIL = PAGE_W - M_L - M_R

EMOJI_RE = re.compile(
    '[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u2705\u274C]'
)

# ---------------------------------------------------------------- fonts
CJK = 'StSongFallback'
CJK_BOLD = 'StSongFallback'
MONO = 'Courier'


def register_fonts():
    global CJK, CJK_BOLD, MONO
    ok = False
    try:
        cjk_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
        if os.path.exists(cjk_path):
            pdfmetrics.registerFont(TTFont('HiraginoGB', cjk_path, subfontIndex=0))
            pdfmetrics.registerFont(TTFont('HiraginoGB-Bold', cjk_path, subfontIndex=1))
            CJK, CJK_BOLD = 'HiraginoGB', 'HiraginoGB-Bold'
            ok = True
    except Exception:
        ok = False
    if not ok:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        CJK = CJK_BOLD = 'STSong-Light'
    try:
        mono_path = '/System/Library/Fonts/Menlo.ttc'
        if os.path.exists(mono_path):
            pdfmetrics.registerFont(TTFont('Menlo', mono_path, subfontIndex=0))
            MONO = 'Menlo'
    except Exception:
        MONO = 'Courier'
    registerFontFamily('BookCJK', normal=CJK, bold=CJK_BOLD, italic=CJK, boldItalic=CJK_BOLD)


def strip_emoji(s):
    return EMOJI_RE.sub('', s).strip()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(s):
    s = strip_emoji(s)
    s = esc(s)
    s = re.sub(r'`([^`]+)`',
               lambda m: '<font face="%s" color="#9d3b34">%s</font>' % (MONO, m.group(1)), s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    return s


def code_line_html(line):
    line = line.replace('\t', '    ')
    m = re.match(r'^( +)', line)
    lead = len(m.group(1)) if m else 0
    body = esc(line[lead:])
    body = re.sub(r'([^\x00-\x7f]+)',
                  lambda mm: '<font face="%s">%s</font>' % (CJK, mm.group(1)), body)
    return '&nbsp;' * lead + body if body else '&nbsp;'


# ---------------------------------------------------------------- styles
S = {}


def make_styles():
    def st(name, **kw):
        kw.setdefault('fontName', CJK)
        S[name] = ParagraphStyle(name, **kw)

    st('CoverKicker', fontSize=13, leading=18, alignment=TA_CENTER, textColor=ACCENT,
       spaceAfter=6)
    st('CoverTitle', fontName=CJK_BOLD, fontSize=30, leading=40, alignment=TA_CENTER,
       textColor=INK, spaceBefore=10, spaceAfter=6)
    st('CoverSub', fontSize=14, leading=22, alignment=TA_CENTER, textColor=BODY_C,
       spaceBefore=6)
    st('CoverMeta', fontSize=9.5, leading=15, alignment=TA_CENTER, textColor=MUTE,
       spaceBefore=18)
    st('Colophon', fontSize=9.5, leading=16, textColor=BODY_C, spaceAfter=3)
    st('ForeTitle', fontName=CJK_BOLD, fontSize=18, leading=26, textColor=INK,
       spaceBefore=6, spaceAfter=12)
    st('body', fontSize=9.5, leading=15.5, textColor=BODY_C, spaceAfter=4, wordWrap='CJK')
    st('AgentTitle', fontName=CJK_BOLD, fontSize=16, leading=22, textColor=INK,
       spaceAfter=10)
    st('h2', fontName=CJK_BOLD, fontSize=12.5, leading=18, textColor=ACCENT,
       spaceBefore=12, spaceAfter=5, wordWrap='CJK')
    st('h3', fontName=CJK_BOLD, fontSize=10.8, leading=16, textColor=INK,
       spaceBefore=9, spaceAfter=4, wordWrap='CJK')
    st('h4', fontName=CJK_BOLD, fontSize=9.8, leading=15, textColor=BODY_C,
       spaceBefore=8, spaceAfter=3, wordWrap='CJK')
    st('bullet', fontSize=9.5, leading=15, textColor=BODY_C, leftIndent=14,
       bulletIndent=4, spaceAfter=2.5, wordWrap='CJK')
    st('bullet2', fontSize=9.5, leading=15, textColor=BODY_C, leftIndent=26,
       bulletIndent=16, spaceAfter=2.5, wordWrap='CJK')
    st('cell', fontSize=8.4, leading=12, textColor=BODY_C, wordWrap='CJK')
    st('cellHead', fontName=CJK_BOLD, fontSize=8.6, leading=12, textColor=INK,
       wordWrap='CJK')
    st('quote', fontSize=9.5, leading=15.5, textColor=colors.HexColor('#6b6459'),
       wordWrap='CJK')
    st('code', fontName=MONO, fontSize=7.6, leading=10.5, textColor=BODY_C)
    st('PartKicker', fontSize=12, leading=16, alignment=TA_CENTER, textColor=ACCENT,
       spaceAfter=8)
    st('PartTitle', fontName=CJK_BOLD, fontSize=24, leading=32, alignment=TA_CENTER,
       textColor=INK, spaceAfter=14)
    st('PartIntro', fontSize=11, leading=18, alignment=TA_CENTER, textColor=BODY_C,
       leftIndent=16, rightIndent=16, wordWrap='CJK')
    st('TOCHead', fontName=CJK_BOLD, fontSize=18, leading=26, textColor=INK, spaceAfter=12)
    st('NoteTitle', fontName=CJK_BOLD, fontSize=13, leading=19, textColor=INK,
       spaceBefore=10, spaceAfter=6)


# ---------------------------------------------------------------- blocks
def code_block(lines):
    if not lines:
        lines = ['']
    html = '<br/>'.join(code_line_html(l) for l in lines)
    t = Table([[Paragraph(html, S['code'])]], colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, CODE_BD),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def quote_block(text):
    t = Table([[Paragraph(inline(text), S['quote'])]], colWidths=[AVAIL - 10])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), QUOTE_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 2.2, ACCENT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def build_table(rows):
    rows = [r for r in rows if r and not all(
        re.fullmatch(r':?-{2,}:?', c or '---') for c in r)]
    if not rows:
        return Spacer(1, 2)
    ncols = max(len(r) for r in rows)
    rows = [r + [''] * (ncols - len(r)) for r in rows]
    data = []
    for ri, r in enumerate(rows):
        style = S['cellHead'] if ri == 0 else S['cell']
        data.append([Paragraph(inline(c), style) for c in r])
    col_w = [AVAIL / ncols] * ncols
    t = Table(data, colWidths=col_w, repeatRows=1, hAlign='LEFT')
    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#efe9e1')),
        ('GRID', (0, 0), (-1, -1), 0.4, CODE_BD),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf9f6')]),
    ]
    t.setStyle(TableStyle(cmds))
    return t


SEP_ROW_RE = re.compile(r'^[-=*_]{3,}$')


def parse_markdown(text, first_h1_style='AgentTitle'):
    flow = []
    lines = text.split('\n')
    if lines and lines[0].strip() == '---':
        try:
            j = lines.index('---', 1)
            lines = lines[j + 1:]
        except ValueError:
            pass
    buf = []
    first_h1_done = False

    def flush():
        nonlocal buf
        if buf:
            flow.append(Paragraph(inline(' '.join(buf)), S['body']))
            flow.append(Spacer(1, 3))
            buf = []

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        s = raw.strip()
        if s.startswith('```'):
            flush()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            flow.append(Spacer(1, 3))
            flow.append(code_block(code))
            flow.append(Spacer(1, 6))
        elif s.startswith('|'):
            flush()
            tbl = []
            while i < n and lines[i].strip().startswith('|'):
                row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                tbl.append(row)
                i += 1
            flow.append(Spacer(1, 3))
            flow.append(build_table(tbl))
            flow.append(Spacer(1, 6))
            continue
        elif s.startswith('#'):
            flush()
            level = len(s) - len(s.lstrip('#'))
            txt = s.lstrip('#').strip()
            if level == 1 and not first_h1_done:
                flow.append(Paragraph(inline(txt), S[first_h1_style]))
                first_h1_done = True
            else:
                key = {1: 'AgentTitle', 2: 'h2', 3: 'h3', 4: 'h4'}.get(level, 'h4')
                flow.append(Paragraph(inline(txt), S[key]))
        elif s.startswith('>'):
            flush()
            q = []
            while i < n and lines[i].strip().startswith('>'):
                q.append(lines[i].strip().lstrip('>').strip())
                i += 1
            flow.append(Spacer(1, 3))
            flow.append(quote_block(' '.join(x for x in q if x)))
            flow.append(Spacer(1, 6))
            continue
        elif re.match(r'^[-*+]\s+', s):
            flush()
            indent = len(raw) - len(raw.lstrip(' '))
            style = S['bullet2'] if indent >= 2 else S['bullet']
            txt = re.sub(r'^[-*+]\s+', '', s)
            flow.append(Paragraph(inline(txt), style, bulletText='•'))
        elif re.match(r'^\d+[.)]\s+', s):
            flush()
            num = re.match(r'^(\d+)[.)]\s+(.*)$', s)
            txt = num.group(2)
            style = S['bullet']
            flow.append(Paragraph(inline(txt), style, bulletText=num.group(1) + '.'))
        elif SEP_ROW_RE.match(s):
            flush()
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width='100%', thickness=0.6, color=CODE_BD,
                                   spaceBefore=2, spaceAfter=6))
        elif s == '':
            flush()
        else:
            buf.append(s)
        i += 1
    flush()
    return flow


# ---------------------------------------------------------------- doc
class BookDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            name = flowable.style.name
            if name == 'PartTitle':
                self.notify('TOCEntry', (0, flowable.getPlainText(), self.page))
            elif name == 'AgentTitle':
                self.notify('TOCEntry', (1, flowable.getPlainText(), self.page))


def on_body_page(canvas, doc):
    canvas.saveState()
    y = 13 * mm
    canvas.setStrokeColor(CODE_BD)
    canvas.setLineWidth(0.5)
    canvas.line(M_L, y, PAGE_W - M_R, y)
    canvas.setFont(CJK, 7.5)
    canvas.setFillColor(MUTE)
    canvas.drawString(M_L, y - 9, BOOK_TITLE)
    canvas.drawRightString(PAGE_W - M_R, y - 9, '%d' % canvas.getPageNumber())
    canvas.restoreState()


def on_cover_page(canvas, doc):
    pass


# ---------------------------------------------------------------- content
PARTS = [
    ('engineering', '工程部',
     '把图纸变成系统。{n} 位工程师覆盖前后端、移动端、DevOps、安全、数据与 AI，'
     '是从“想清楚了”走到“跑起来了”的主力部队。'),
    ('design', '设计部',
     '从“能用”到“想用”。{n} 位设计师负责品牌、界面、体验研究与视觉叙事，'
     '让产品在被使用之前先被相信。'),
    ('product', '产品部',
     '决定做什么、不做什么。{n} 位产品角色把模糊的机会变成有优先级的路线图，'
     '和经得起追问的需求文档。'),
    ('project-management', '项目管理部',
     '让承诺可兑现。{n} 位管理者守范围、排依赖、控风险，'
     '用仪式和看板代替人肉跟踪。'),
    ('testing', '测试部',
     '交付前的最后一道闸。{n} 位质量专家从无障碍、API、性能到“现实检查”，'
     '专门戳破“看起来好了”。'),
    ('specialized', '特殊专家部',
     '疑难杂症科。{n} 位跨领域专家，从供应链、招聘、政务合规到区块链审计'
     '与多智能体信任架构。'),
    ('marketing', '营销部',
     '让产品被看见。{n} 位营销角色覆盖中外各平台的内容、增长与品牌打法。'),
    ('paid-media', '付费媒体部',
     '花出去的每一分钱都要算。{n} 位投放专家管理跨平台预算、追踪与持续优化。'),
    ('sales', '销售部',
     '把兴趣变成合同。{n} 位销售角色从线索挖掘到管道分析，从谈判复盘到销售教练。'),
    ('support', '支持部',
     '留住已经赢得的客户。{n} 位支持角色覆盖客服、财务、法务与合规。'),
    ('spatial-computing', '空间计算部',
     '下一代界面。{n} 位空间计算工程师深耕 visionOS、WebXR 与 Metal 渲染。'),
    ('game-development', '游戏开发部',
     '跨引擎作战。{n} 位游戏开发专家覆盖 Unity、Unreal、Godot、Roblox 与 Blender。'),
    ('academic', '学术部',
     '世界观的守门人。{n} 位学者为虚构世界把守人类学、地理、历史、叙事'
     '与心理的一致性。'),
]

STORY_INTRO = ('终章不介绍新的智能体，而是让前面出场的专家真正动起来：'
               '星舟科技要上线一个优惠券功能，六幕剧依次展示产品经理、架构师、'
               '后端、设计师、前端、代码评审与 DevOps 如何接力交付——'
               '每一棒的交接物，都是下一棒的输入。这是全书红线的最终证明。')


def md_files(d):
    d = os.path.join(USAGE, d)
    return sorted(f for f in os.listdir(d) if f.endswith('.md'))


def para(text, style='body'):
    return Paragraph(inline(text), S[style])


def build_story_flow():
    story = []

    # 封面
    story.append(NextPageTemplate('Cover'))
    story.append(Spacer(1, 60 * mm))
    story.append(para('THE AGENCY AGENT LIBRARY', 'CoverKicker'))
    story.append(Paragraph('<b>智能体实战手册</b>', S['CoverTitle']))
    story.append(para('148 位专家智能体的雇佣指南', 'CoverSub'))
    story.append(Spacer(1, 16 * mm))
    story.append(HRFlowable(width='30%', thickness=1.2, color=ACCENT, hAlign='CENTER'))
    story.append(Spacer(1, 14 * mm))
    story.append(para('基于 docs/usage 全量使用文档汇编 · 分支 ' + BRANCH, 'CoverMeta'))
    story.append(para('Version %s · %s · Book Co-Author 执笔汇编' % (VERSION, DATE),
                      'CoverMeta'))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # 版权页
    story.append(para('版权与版本', 'ForeTitle'))
    colophon = [
        ('书名', BOOK_TITLE),
        ('编著', 'The Agency × Book Co-Author'),
        ('版本', '%s - ready for approval' % VERSION),
        ('编译日期', DATE),
        ('素材来源', 'docs/usage/（%s 分支下的全量 Markdown 使用文档）' % BRANCH),
        ('版权说明', '本手册为 The Agency 仓库使用文档的汇编，随仓库开源协议一同发布。'),
    ]
    story.append(build_table([[k, v] for k, v in colophon]))
    story.append(Spacer(1, 10))
    story.append(para('本书按“建造 → 验证 → 增长 → 前沿”的顺序重排部门，'
                      '使阅读路径与一个产品的真实生命周期一致。', 'body'))
    story.append(PageBreak())

    # 前言
    story.append(para('前言：这是一本关于“雇佣”的书', 'ForeTitle'))
    foreword = [
        '这不是一本讲 AI 原理的书，是一本关于“雇佣”的书。The Agency 收录了'
        '一百多位性格分明、各管一摊的专家智能体，本书为其中每一位撰写了一份'
        '使用文档：他是谁、有什么铁律、什么时候雇佣他、两个具体颗粒度的实战'
        '案例、使用技巧，以及他与其他同事的交接关系。',
        '贯穿全书的红线只有一条：智能体的价值不在人设本身，而在“接活与交活”'
        '的接力。单独看，每位专家只解决一类问题；串起来，他们就是一支能从需求'
        '走到上线、从上线走到增长的交付团队。终章用一个完整的工程故事——'
        '星舟科技的优惠券功能——把这条红线变成可以照着组装的样板。',
        '使用建议：先看下一页的全书导航找到你关心的部门；进入某个智能体的'
        '章节后，顺着文末的“与其他 Agent 的接力”跨部门跳转，那才是这本手册'
        '正确的打开方式。',
        '需要说明的一点：案例中的公司、数据与对话，是为说明工作方法而构造的'
        '还原性场景，数字不必较真，方法论与模板可以直接复用。',
    ]
    for p in foreword:
        story.append(para(p))
        story.append(Spacer(1, 4))

    # 全书导航
    story.append(para('全书导航', 'NoteTitle'))
    nav = [['部门', '专家数', '阅读起点']]
    total = 0
    counts = {}
    for d, zh, intro in PARTS:
        c = len(md_files(d))
        counts[d] = c
        total += c
        nav.append([zh, str(c), intro.replace('{n} 位', '').split('。')[0]])
    nav.append(['终章（跨部门故事）', '1', '六幕剧：一次完整的接力交付'])
    story.append(build_table(nav))
    story.append(Spacer(1, 6))
    story.append(para('合计 %d 位专家智能体 + 1 篇跨部门工程故事。' % total))
    story.append(PageBreak())

    # 目录
    story.append(para('目录', 'TOCHead'))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle('TOCPart', fontName=CJK_BOLD, fontSize=11, leading=18,
                       spaceBefore=10, textColor=ACCENT, wordWrap='CJK'),
        ParagraphStyle('TOCAgent', fontName=CJK, fontSize=9.2, leading=13.6,
                       leftIndent=14, textColor=BODY_C, wordWrap='CJK'),
    ]
    toc.dotsMinLevel = 1
    story.append(toc)
    story.append(PageBreak())

    # 各部门
    for idx, (d, zh, intro) in enumerate(PARTS, 1):
        story.append(Spacer(1, 50 * mm))
        story.append(para('PART %02d' % idx, 'PartKicker'))
        story.append(Paragraph('<b>%s</b>' % esc(zh), S['PartTitle']))
        story.append(para(intro.replace('{n}', str(counts[d])), 'PartIntro'))
        story.append(PageBreak())
        for f in md_files(d):
            text = open(os.path.join(USAGE, d, f), encoding='utf-8').read()
            story.append(PageBreak())
            story.extend(parse_markdown(text))

    # 终章
    story.append(Spacer(1, 50 * mm))
    story.append(para('FINALE', 'PartKicker'))
    story.append(Paragraph('<b>终章：一个完整的工程故事</b>', S['PartTitle']))
    story.append(para(STORY_INTRO, 'PartIntro'))
    story.append(PageBreak())
    story_path = os.path.join(USAGE, 'story-cross-team-feature.md')
    if os.path.exists(story_path):
        text = open(story_path, encoding='utf-8').read()
        story.extend(parse_markdown(text))

    # 编辑手记
    story.append(PageBreak())
    story.append(para('编辑手记（Editorial Notes）', 'ForeTitle'))
    notes = [
        '版本：%s - ready for approval。本书为 docs/usage 全量文档的首次成书汇编。' % VERSION,
        '假设：部门顺序按“建造 → 验证 → 增长 → 前沿”重排，与目录的原始字母序不同；'
        '全部案例均来自各智能体使用文档原文，仅做图书化排版。',
        '证据缺口：案例中的数字为构造场景，非真实项目审计数据；如需引用请回溯'
        '对应 Markdown 文档核实。',
        '待作者决定：是否为每个部门补写一篇部门级串联故事；书名、封面风格与'
        '是否收入 strategy/ 目录下的 NEXUS 编排内容。',
    ]
    for x in notes:
        story.append(Paragraph(inline(x), S['bullet'], bulletText='•'))
    story.append(Spacer(1, 10))
    story.append(para('下一轮修订建议：先通读终章，再决定第一优先补写哪个部门的'
                      '串联故事。', 'body'))
    return story


def main():
    register_fonts()
    make_styles()
    doc = BookDoc(OUT, pagesize=A4,
                  leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                  title=BOOK_TITLE, author='The Agency × Book Co-Author',
                  subject='148 位专家智能体的雇佣指南')
    body_frame = Frame(M_L, M_B, AVAIL, PAGE_H - M_T - M_B, id='body')
    cover_frame = Frame(M_L, M_B, AVAIL, PAGE_H - M_T - M_B, id='cover')
    doc.addPageTemplates([
        PageTemplate(id='Body', frames=[body_frame], onPage=on_body_page),
        PageTemplate(id='Cover', frames=[cover_frame], onPage=on_cover_page),
    ])
    flow = build_story_flow()
    doc.multiBuild(flow)
    print('OK ->', OUT)


if __name__ == '__main__':
    main()
