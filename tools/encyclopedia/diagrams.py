"""Render declarative diagrams to SVG.

A step with no picture is just prose in a box, so every step is expected to
carry a *visual* -- one of four primitives, chosen to fit what that stage of the
process actually is:

    grid    labelled rows of cells        state that accumulates
    bars    proportional meters           one resource saturated, another idle
    fan     one source, many targets      attention, dispatch, broadcast
    chips   a sequence of tokens          a stream, with the new item marked

Plus a `flow` diagram for pipelines and loops.

Colour is carried by CSS classes rather than attributes, so dark mode and the
site palette apply without regenerating anything. The accent marks exactly what
changed at this step; if everything is marked, nothing is.
"""

from __future__ import annotations

from html import escape
from typing import Any

W = 960
PAD = 20

STEP_PAD = 20
STEP_GAP = 12
NUM_X = 40
TITLE_X = 68
NOTE_LEAD = 21

VIS_W = 640          # the visual leads; text is a caption on it
CELL_W = 78
CELL_H = 42
CELL_GAP = 8
ROW_GAP = 8
LABEL_GAP = 10

MONO_ADV = 7.4
SANS_ADV = 7.0

FOOTER_LEAD = 17
FOOTER_ADV = 6.4          # JetBrains Mono at 11.5px


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------

def _t(x: float, y: float, text: str, cls: str, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" class="{cls}" text-anchor="{anchor}">'
        f"{escape(str(text))}</text>"
    )


def _arrow(x1: float, y1: float, x2: float, y2: float | None = None, cls: str = "dgm-arrow") -> str:
    y2 = y1 if y2 is None else y2
    return (
        f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
        f'class="{cls}" marker-end="url(#dgm-head)"/>'
    )


def _cell(x: float, y: float, text: str, new: bool, w: float = CELL_W, h: float = CELL_H) -> str:
    cls = "dgm-cell dgm-cell--new" if new else "dgm-cell"
    tcls = "dgm-celltext dgm-celltext--new" if new else "dgm-celltext"
    return (
        f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="3" class="{cls}"/>'
        + _t(x + w / 2, y + h / 2 + 4, text, tcls, "middle")
    )


def _unpack(cell: Any) -> tuple[str, bool]:
    if isinstance(cell, dict):
        return str(cell.get("text", "")), bool(cell.get("new"))
    return str(cell), False



CAP_LEAD = 16


def _caption(spec: dict[str, Any], x: float, y: float,
             width: float | None = None) -> tuple[str, float]:
    """The line under a visual, wrapped.

    Captions were emitted as one unbroken run, exactly as footers were, so a
    caption longer than the canvas simply left the frame. Every primitive routes
    through here now, which is why there is one function rather than sixteen
    near-identical three-line blocks.
    """
    text = spec.get("caption")
    if not text:
        return "", 0.0
    # Visuals are centred, so the room a caption has is measured from wherever
    # it actually starts — not from the left edge of the canvas.
    if width is None:
        width = max(240.0, W - PAD - x)
    lines = _wrap_text(str(text), width, 12.5)
    return _text_block(x, y, lines, "dgm-caption", CAP_LEAD), (len(lines) - 1) * CAP_LEAD


# --------------------------------------------------------------------------
# visuals — each returns (markup, height)
# --------------------------------------------------------------------------

CHIP_MIN_W = 74
CHIP_PAD = 22


def _chip_w(item: Any) -> float:
    """A chip is as wide as its word. Fixed-width chips silently clipped
    anything past nine characters, which quietly shortened the vocabulary."""
    text, _ = _unpack(item)
    return max(CHIP_MIN_W, len(text) * MONO_ADV + CHIP_PAD)


def _vis_grid(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    rows = spec.get("rows", [])
    label_w = max((len(str(r.get("label", ""))) * MONO_ADV for r in rows), default=0)
    cells_x = x + label_w + LABEL_GAP
    out: list[str] = []
    cy = y
    for row in rows:
        if row.get("label"):
            out.append(_t(cells_x - LABEL_GAP, cy + CELL_H / 2 + 4, row["label"], "dgm-rowlabel", "end"))
        cx = cells_x
        for cell in row.get("cells", []):
            text, new = _unpack(cell)
            out.append(_cell(cx, cy, text, new))
            cx += CELL_W + CELL_GAP
        cy += CELL_H + ROW_GAP
    height = max(cy - y - ROW_GAP, 0)
    cap, cap_extra = _caption(spec, cells_x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


def _vis_bars(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """Proportional meters. The clearest way to show 'this is saturated and
    that is idle', which is the whole story of memory-bound work."""
    bars = spec.get("bars", [])
    label_w = max((len(str(b.get("label", ""))) * MONO_ADV for b in bars), default=0)
    track_x = x + label_w + LABEL_GAP
    track_w = VIS_W - label_w - LABEL_GAP - 90
    out: list[str] = []
    cy = y + 6
    for bar in bars:
        pct = max(0.0, min(1.0, float(bar.get("value", 0))))
        full = bool(bar.get("accent"))
        out.append(_t(track_x - LABEL_GAP, cy + 14, bar.get("label", ""), "dgm-rowlabel", "end"))
        out.append(
            f'<rect x="{track_x:.0f}" y="{cy:.0f}" width="{track_w:.0f}" height="18" '
            f'rx="4" class="dgm-track"/>'
        )
        out.append(
            f'<rect x="{track_x:.0f}" y="{cy:.0f}" width="{track_w * pct:.0f}" height="18" '
            f'rx="3" class="{"dgm-fill dgm-fill--accent" if full else "dgm-fill"}"/>'
        )
        if bar.get("value_label"):
            out.append(_t(track_x + track_w + 10, cy + 14, bar["value_label"], "dgm-barvalue"))
        cy += 32
    height = cy - y
    cap, cap_extra = _caption(spec, track_x, y + height + 14)
    if cap:
        out.append(cap)
        height += 20 + cap_extra
    return "\n".join(out), height


def _vis_fan(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """One source connected to many targets — attention over a cache, a router
    dispatching, a broadcast."""
    source = spec.get("source", "")
    targets = spec.get("targets", [])
    n = max(len(targets), 1)
    src_w = max(68, len(str(source)) * MONO_ADV + CHIP_PAD)
    src_h = 38
    tgt_h = 30
    tgt_w = max((_chip_w(t) for t in targets), default=78)
    gap = 8
    total_h = n * tgt_h + (n - 1) * gap
    src_y = y + total_h / 2 - src_h / 2
    tgt_x = x + src_w + 110
    out = [_cell(x, src_y, source, True, src_w, src_h)]
    cy = y
    for target in targets:
        text, new = _unpack(target)
        out.append(
            f'<path d="M {x + src_w + 4:.0f} {src_y + src_h / 2:.0f} '
            f'C {x + src_w + 40:.0f} {src_y + src_h / 2:.0f}, '
            f'{tgt_x - 34:.0f} {cy + tgt_h / 2:.0f}, {tgt_x - 6:.0f} {cy + tgt_h / 2:.0f}" '
            f'class="dgm-fanline"/>'
        )
        out.append(_cell(tgt_x, cy, text, new, tgt_w, tgt_h))
        cy += tgt_h + gap
    cap, cap_extra = _caption(spec, x, y + total_h + 16)
    if cap:
        out.append(cap)
        total_h += 20 + cap_extra
    return "\n".join(out), total_h


def _vis_chips(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """A short sequence, optionally with a return arrow — a token stream."""
    items = spec.get("items", [])
    ch, gap = 34, 12
    widths = [_chip_w(item) for item in items]
    out: list[str] = []
    cx = x
    first_mid = x + (widths[0] / 2 if widths else 0)
    last_mid = x
    for i, item in enumerate(items):
        text, new = _unpack(item)
        cw = widths[i]
        out.append(_cell(cx, y, text, new, cw, ch))
        last_mid = cx + cw / 2
        if i < len(items) - 1:
            out.append(_arrow(cx + cw + 1, y + ch / 2, cx + cw + gap - 1))
        cx += cw + gap
    height = ch
    if spec.get("loop"):
        ly = y + ch + 16
        out.append(
            f'<path d="M {last_mid:.0f} {y + ch + 2:.0f} '
            f'L {last_mid:.0f} {ly:.0f} L {first_mid:.0f} {ly:.0f} '
            f'L {first_mid:.0f} {y + ch + 6:.0f}" '
            f'class="dgm-arrow dgm-arrow--loop" marker-end="url(#dgm-head)"/>'
        )
        loop_lines = _wrap_text(str(spec["loop"]), max(240.0, W - PAD - x), 12.5)
        out.append(_text_block(x, ly + 26, loop_lines, "dgm-caption", CAP_LEAD))
        height = ly - y + 32 + (len(loop_lines) - 1) * CAP_LEAD
    else:
        cap, cap_extra = _caption(spec, x, y + ch + 16)
        if cap:
            out.append(cap)
            height = ch + 20 + cap_extra
    return "\n".join(out), height


def _vis_stack(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """Layered bands — a stack of tiers, read top to bottom. Covers memory
    hierarchies, system layers, pipelines drawn as levels."""
    layers = spec.get("layers", [])
    w = spec.get("width", VIS_W)
    label_w = max((len(str(lay.get("label", ""))) * MONO_ADV for lay in layers), default=0)
    band_x = x + label_w + LABEL_GAP
    band_w = w - label_w - LABEL_GAP
    out: list[str] = []
    cy = y
    for layer in layers:
        tone = _tone(layer)
        note = str(layer.get("note", ""))
        # The note is right-aligned inside the band, so the text only gets what
        # the note leaves. Measuring that up front is what stops a long band
        # text from running straight through its own note.
        note_w = (_w_mono(note) + 20) if note else 0
        text_lines = _wrap_text(layer.get("text", ""), band_w - 28 - note_w, 13.5, bold=True)
        h = max(40.0, 16 + len(text_lines) * 19)
        out.append(
            f'<rect x="{band_x:.0f}" y="{cy:.0f}" width="{band_w:.0f}" height="{h:.0f}" '
            f'rx="4" class="{_cls("dgm-band", tone)}"/>'
        )
        if layer.get("label"):
            out.append(_t(band_x - LABEL_GAP, cy + h / 2 + 5, layer["label"],
                          _cls("dgm-rowlabel", tone), "end"))
        ty = cy + h / 2 + 5 - (len(text_lines) - 1) * 9.5
        out.append(_text_block(band_x + 14, ty, text_lines, _cls("dgm-bandtext", tone), 19))
        if note:
            out.append(_t(band_x + band_w - 14, cy + h / 2 + 5, note, "dgm-bandnote", "end"))
        cy += h + 6
    height = cy - y - 6
    cap, cap_extra = _caption(spec, band_x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


def _vis_columns(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """Two or three columns side by side — before and after, this versus that."""
    cols = spec.get("columns", [])
    n = max(len(cols), 1)
    w = spec.get("width", VIS_W)
    gap = 18
    col_w = (w - gap * (n - 1)) / n
    rows = max((len(c.get("lines", [])) for c in cols), default=0)
    head_h = 34
    height = head_h + rows * 24 + 16
    out: list[str] = []
    for i, col in enumerate(cols):
        cx = x + i * (col_w + gap)
        tone = _tone(col)
        out.append(
            f'<rect x="{cx:.0f}" y="{y:.0f}" width="{col_w:.0f}" height="{height:.0f}" '
            f'rx="5" class="{_cls("dgm-col", tone)}"/>'
        )
        out.append(_t(cx + col_w / 2, y + 22, col.get("title", ""),
                      _cls("dgm-coltitle", tone), "middle"))
        out.append(
            f'<line x1="{cx + 10:.0f}" y1="{y + head_h - 4:.0f}" '
            f'x2="{cx + col_w - 10:.0f}" y2="{y + head_h - 4:.0f}" class="dgm-rule"/>'
        )
        ly = y + head_h + 18
        for line in col.get("lines", []):
            out.append(_t(cx + col_w / 2, ly, line, "dgm-colline", "middle"))
            ly += 24
    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


def _vis_table(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    """A small matrix of values — comparison grids and lookup shapes."""
    head = spec.get("head", [])
    rows = spec.get("rows", [])
    ncol = max(len(head), max((len(r) for r in rows), default=0))
    w = spec.get("width", VIS_W)
    first_w = w * 0.34 if ncol > 1 else w
    cell_w = (w - first_w) / max(ncol - 1, 1)
    rh = 32
    out: list[str] = []
    cy = y
    if head:
        for i, cell in enumerate(head):
            cx = x if i == 0 else x + first_w + (i - 1) * cell_w
            cw = first_w if i == 0 else cell_w
            out.append(_t(cx + (10 if i == 0 else cw / 2), cy + 20,
                          cell, "dgm-thead", "start" if i == 0 else "middle"))
        cy += rh
        out.append(f'<line x1="{x:.0f}" y1="{cy - 8:.0f}" x2="{x + w:.0f}" '
                   f'y2="{cy - 8:.0f}" class="dgm-rule"/>')
    for row in rows:
        # Measure every cell first, so the row is tall enough for its longest.
        wrapped = []
        for i, cell in enumerate(row):
            text, new = _unpack(cell)
            cw = first_w if i == 0 else cell_w
            wrapped.append((_wrap_text(text, cw - 20, 13, mono=True), new, cw))
        lines = max((len(c[0]) for c in wrapped), default=1)
        row_h = max(rh, 12 + lines * 19)
        for i, (cell_lines, new, cw) in enumerate(wrapped):
            cx = x if i == 0 else x + first_w + (i - 1) * cell_w
            cls = "dgm-tcell--new" if new else ("dgm-tcell--lead" if i == 0 else "dgm-tcell")
            anchor = "start" if i == 0 else "middle"
            tx = cx + (10 if i == 0 else cw / 2)
            for j, line in enumerate(cell_lines):
                out.append(_t(tx, cy + 20 + j * 19, line, cls, anchor))
        cy += row_h
        out.append(f'<line x1="{x:.0f}" y1="{cy - 8:.0f}" x2="{x + w:.0f}" '
                   f'y2="{cy - 8:.0f}" class="dgm-rule dgm-rule--soft"/>')
    height = cy - y
    cap, cap_extra = _caption(spec, x, y + height + 14)
    if cap:
        out.append(cap)
        height += 20 + cap_extra
    return "\n".join(out), height




# --------------------------------------------------------------------------
# tone — semantic colour, one meaning per hue
#
#   (none)   context. The parts of the picture that are just there.
#   accent   the subject. What this step changed, or what the reader came for.
#   warn     a cost, a limit, a thing that saturates.
#   bad      the failure case in a right/wrong pair.
#   ok       the success case in a right/wrong pair.
#
# At most one accent per figure. If everything is marked, nothing is.
# --------------------------------------------------------------------------

TONES = ("accent", "warn", "bad", "ok", "muted")


def _tone(spec: Any, default: str = "") -> str:
    """Read a tone off a spec dict, accepting `new: true` as a legacy alias."""
    if not isinstance(spec, dict):
        return default
    tone = spec.get("tone")
    if tone in TONES:
        return str(tone)
    if spec.get("accent") or spec.get("new"):
        return "accent"
    return default


def _cls(base: str, tone: str) -> str:
    return f"{base} {base}--{tone}" if tone else base


def _w_mono(text: Any) -> float:
    return len(str(text)) * MONO_ADV


def _w_sans(text: Any, size: float = 13.5) -> float:
    return len(str(text)) * (SANS_ADV * size / 13.5)


def _text_block(x: float, y: float, lines: list[str], cls: str,
                lead: float = 17, anchor: str = "start") -> str:
    return "\n".join(_t(x, y + i * lead, ln, cls, anchor) for i, ln in enumerate(lines))


BOLD_FACTOR = 1.09        # semibold is about nine per cent wider than regular


def _wrap_text(text: str, width: float, size: float = 13.5,
               mono: bool = False, bold: bool = False) -> list[str]:
    """Greedy wrap at an approximate advance width.

    Mono is measured with the mono advance; wrapping a monospaced string against
    a proportional estimate under-counts by about fifteen per cent, which is
    exactly enough to push the last word through the side of its box. Semibold
    runs about nine per cent wide of regular, and misses by the same one word.
    """
    adv = (MONO_ADV if mono else SANS_ADV) * size / 13.5
    if bold:
        adv *= BOLD_FACTOR
    out: list[str] = []
    line = ""
    for word in str(text).split():
        candidate = (line + " " + word).strip()
        if len(candidate) * adv > width and line:
            out.append(line)
            line = word
        else:
            line = candidate
    if line:
        out.append(line)
    return out


# --------------------------------------------------------------------------
# segments — one quantity, divided
#
# A single bar cut into proportional named parts. This is the right picture
# whenever the story is "a fixed budget, and here is what is spending it":
# a context window, a token budget, a latency breakdown, a training mixture.
# --------------------------------------------------------------------------

SEG_H = 52
SEG_LABEL_LEAD = 16


def _vis_segments(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    segs = spec.get("segments", [])
    if not segs:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    total = sum(max(float(s.get("value", 1)), 0.0001) for s in segs) or 1.0

    out: list[str] = []
    top = y
    if spec.get("label"):
        out.append(_t(x + w, top + 10, spec["label"], "dgm-seglabel", "end"))
        top += 18

    # the bar itself
    out.append(
        f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{SEG_H}" '
        f'rx="5" class="dgm-segtrack"/>'
    )

    edges: list[tuple[float, float, dict[str, Any]]] = []
    cx = x
    for seg in segs:
        sw = w * (max(float(seg.get("value", 1)), 0.0001) / total)
        edges.append((cx, sw, seg))
        cx += sw

    for i, (sx, sw, seg) in enumerate(edges):
        tone = _tone(seg)
        # Untoned segments step through four neutral weights so neighbours
        # separate without introducing colour that would mean something.
        shade = "" if tone else f' fill-opacity="{0.20 + 0.06 * (i % 3):.2f}"'
        out.append(
            f'<rect x="{sx:.1f}" y="{top:.0f}" width="{sw:.1f}" height="{SEG_H}" '
            f'class="{_cls("dgm-seg", tone)}"{shade}/>'
        )
        if i:
            out.append(
                f'<line x1="{sx:.1f}" y1="{top:.0f}" x2="{sx:.1f}" '
                f'y2="{top + SEG_H:.0f}" class="dgm-segdiv"/>'
            )
        if seg.get("value_label") and sw > _w_mono(seg["value_label"]) + 14:
            out.append(
                _t(sx + sw / 2, top + SEG_H / 2 + 5, seg["value_label"],
                   _cls("dgm-segvalue", tone), "middle")
            )

    out.append(
        f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{SEG_H}" '
        f'rx="5" class="dgm-segframe"/>'
    )

    # Labels sit below the bar on staggered rows, each on a leader line, so a
    # thin segment is still nameable without shrinking its type.
    rows_right: list[float] = []
    label_y0 = top + SEG_H + 18
    max_row = 0
    for sx, sw, seg in edges:
        text = str(seg.get("text", ""))
        if not text:
            continue
        tw = _w_sans(text, 12.5)
        centre = sx + sw / 2
        left = max(x, min(centre - tw / 2, x + w - tw))
        row = 0
        while row < len(rows_right) and left < rows_right[row] + 12:
            row += 1
        if row == len(rows_right):
            rows_right.append(left + tw)
        else:
            rows_right[row] = left + tw
        max_row = max(max_row, row)
        ly = label_y0 + row * SEG_LABEL_LEAD
        out.append(
            f'<path d="M {centre:.1f} {top + SEG_H:.0f} L {centre:.1f} '
            f'{ly - 10:.0f}" class="dgm-leader"/>'
        )
        out.append(_t(left + tw / 2, ly, text, _cls("dgm-seglabeltext", _tone(seg)), "middle"))

    height = label_y0 + max_row * SEG_LABEL_LEAD + 6 - y

    # optional span brackets, e.g. "these three are cacheable"
    for span in spec.get("spans", []):
        i0 = int(span.get("from", 0))
        i1 = int(span.get("to", i0))
        i0 = max(0, min(i0, len(edges) - 1))
        i1 = max(i0, min(i1, len(edges) - 1))
        sx = edges[i0][0]
        ex = edges[i1][0] + edges[i1][1]
        by = y + height + 8
        out.append(
            f'<path d="M {sx:.1f} {by:.0f} L {sx:.1f} {by + 6:.0f} '
            f'L {ex:.1f} {by + 6:.0f} L {ex:.1f} {by:.0f}" '
            f'class="{_cls("dgm-span", _tone(span))}"/>'
        )
        out.append(
            _t((sx + ex) / 2, by + 22, span.get("text", ""),
               _cls("dgm-spantext", _tone(span)), "middle")
        )
        height += 34

    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# plot — a curve, on axes
#
# The one primitive that shows a *shape*: how an activation bends, where a
# score saturates, how loss falls with compute. Points are given in data
# coordinates and mapped here, so the spec stays readable.
# --------------------------------------------------------------------------

PLOT_H = 200


def _vis_plot(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    curves = spec.get("curves", [])
    w = float(spec.get("width", VIS_W))
    h = float(spec.get("height", PLOT_H))

    pts_all = [p for c in curves for p in c.get("points", [])]
    if not pts_all:
        return "", 0.0
    xs = [float(p[0]) for p in pts_all]
    ys = [float(p[1]) for p in pts_all]
    xr = spec.get("x_range") or [min(xs), max(xs)]
    yr = spec.get("y_range") or [min(ys), max(ys)]
    x0, x1 = float(xr[0]), float(xr[1])
    y0, y1 = float(yr[0]), float(yr[1])
    if x1 == x0:
        x1 = x0 + 1
    if y1 == y0:
        y1 = y0 + 1

    labelled = [c for c in curves if c.get("label")]
    gutter = 8 + max((_w_sans(c["label"], 12.5) for c in labelled), default=0)
    left = x + (30 if spec.get("y_label") else 4)
    right = x + w - gutter
    plot_w = right - left

    def px(v: float) -> float:
        return left + (float(v) - x0) / (x1 - x0) * plot_w

    def py(v: float) -> float:
        return y + h - (float(v) - y0) / (y1 - y0) * h

    # A clip so a curve that leaves the stated range is cut at the frame rather
    # than drawn across the rest of the page.
    # Derived from the geometry, not from hash(): builds must be byte-identical
    # run to run, and two plots with the same frame can safely share one clip.
    cid = f"dgm-clip-{left:.0f}-{y:.0f}-{plot_w:.0f}-{h:.0f}".replace("-", "n").replace(".", "")
    cid = "dgm-clip-" + cid[9:]
    out = [
        f'<defs><clipPath id="{cid}">'
        f'<rect x="{left:.1f}" y="{y:.0f}" width="{plot_w:.1f}" height="{h:.0f}"/>'
        f"</clipPath></defs>",
        f'<rect x="{left:.1f}" y="{y:.0f}" width="{plot_w:.1f}" height="{h:.0f}" '
        f'rx="4" class="dgm-plotframe"/>',
    ]

    for band in spec.get("bands", []):
        bx0, bx1 = px(band["from"]), px(band["to"])
        out.append(
            f'<rect x="{bx0:.1f}" y="{y:.0f}" width="{bx1 - bx0:.1f}" '
            f'height="{h:.0f}" class="{_cls("dgm-plotband", _tone(band))}"/>'
        )
        if band.get("text"):
            out.append(_t((bx0 + bx1) / 2, y + 15, band["text"],
                          "dgm-plotband-text", "middle"))

    # axes only where zero actually falls inside the range
    if y0 <= 0 <= y1:
        out.append(f'<line x1="{left:.1f}" y1="{py(0):.1f}" x2="{right:.1f}" '
                   f'y2="{py(0):.1f}" class="dgm-axis"/>')
    if x0 <= 0 <= x1:
        out.append(f'<line x1="{px(0):.1f}" y1="{y:.0f}" x2="{px(0):.1f}" '
                   f'y2="{y + h:.0f}" class="dgm-axis"/>')

    body: list[str] = []
    ends: list[tuple[float, dict[str, Any]]] = []
    for i, cv in enumerate(curves):
        pts = cv.get("points", [])
        if not pts:
            continue
        d = " ".join(
            ("M" if j == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
            for j, p in enumerate(pts)
        )
        body.append(f'<path d="{d}" class="{_cls("dgm-curve", _tone(cv))}" style="--i:{i}"/>')
        if cv.get("label"):
            ends.append((min(max(py(pts[-1][1]), y + 6), y + h - 2), cv))
    out.append(f'<g clip-path="url(#{cid})">{chr(10).join(body)}</g>')

    # Labels ride at the end of their own curve. Where two curves finish close
    # together the labels are pushed apart rather than overprinted.
    ends.sort(key=lambda e: e[0])
    placed: list[float] = []
    for ly, cv in ends:
        while placed and ly - placed[-1] < 15:
            ly = placed[-1] + 15
        placed.append(ly)
        out.append(_t(right + 8, ly + 4, cv["label"], _cls("dgm-curvelabel", _tone(cv))))

    for mark in spec.get("marks", []):
        mx, my = px(mark["at"][0]), py(mark["at"][1])
        tone = _tone(mark, "accent")
        out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.5" '
                   f'class="{_cls("dgm-mark", tone)}"/>')
        if mark.get("text"):
            dy = float(mark.get("dy", -14))
            dx = float(mark.get("dx", 0))
            anchor = mark.get("anchor", "middle")
            out.append(
                f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{mx + dx:.1f}" '
                f'y2="{my + dy + (5 if dy < 0 else -5):.1f}" class="dgm-leader"/>'
            )
            out.append(_t(mx + dx, my + dy, mark["text"],
                          _cls("dgm-marktext", tone), anchor))

    height = h
    if spec.get("x_label"):
        out.append(_t(right, y + h + 16, spec["x_label"], "dgm-axislabel", "end"))
        height += 20
    if spec.get("y_label"):
        cy = y + h / 2
        out.append(
            f'<text x="{x + 10:.0f}" y="{cy:.0f}" class="dgm-axislabel" '
            f'text-anchor="middle" transform="rotate(-90 {x + 10:.0f} {cy:.0f})">'
            f"{escape(str(spec['y_label']))}</text>"
        )
    cap, cap_extra = _caption(spec, left, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# passes — one path, travelled twice
#
# Forward above, backward below, over a shared row of stages. Built for
# backpropagation, and for anything else where the return trip is the point.
# --------------------------------------------------------------------------

def _vis_passes(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    nodes = spec.get("nodes", [])
    n = len(nodes)
    if not n:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    gap = 22
    bw = (w - gap * (n - 1)) / n
    bh = 44
    lane = 46            # room for the lane label *and* the notes beneath it
    top = y + lane
    out: list[str] = []

    fwd = spec.get("forward") or {}
    back = spec.get("backward") or {}

    if fwd.get("label"):
        out.append(_t(x, y + 11, fwd["label"], "dgm-lanelabel"))
    for i, node in enumerate(nodes):
        nx = x + i * (bw + gap)
        tone = _tone(node)
        text = node.get("text", "") if isinstance(node, dict) else str(node)
        out.append(
            f'<rect x="{nx:.1f}" y="{top:.0f}" width="{bw:.1f}" height="{bh}" '
            f'rx="5" class="{_cls("dgm-box", tone)}"/>'
        )
        out.append(_t(nx + bw / 2, top + bh / 2 + 5, text,
                      _cls("dgm-boxtitle", tone), "middle"))
        if isinstance(node, dict) and node.get("note"):
            out.append(_t(nx + bw / 2, top - 10, node["note"], "dgm-boxnote", "middle"))
        if i < n - 1:
            mx = nx + bw
            out.append(_arrow(mx + 4, top + bh / 2, mx + gap - 5))

    height = top + bh - y

    if back:
        by = top + bh + 38
        labels = back.get("marks", [])
        # One unbroken line, because it is one pass. The marks name what is
        # computed as it travels, rather than chopping it into separate arrows.
        out.append(
            f'<line x1="{x + w:.1f}" y1="{by:.0f}" x2="{x:.1f}" y2="{by:.0f}" '
            f'class="dgm-arrow dgm-arrow--back" marker-end="url(#dgm-head)"/>'
        )
        for i, label in enumerate(labels[: n - 1]):
            nx = x + i * (bw + gap)
            out.append(_t(nx + bw / 2 + gap / 2, by - 11, label,
                          "dgm-passmark", "middle"))
            out.append(
                f'<line x1="{nx + bw / 2 + gap / 2:.1f}" y1="{top + bh:.0f}" '
                f'x2="{nx + bw / 2 + gap / 2:.1f}" y2="{by - 20:.0f}" '
                f'class="dgm-leader"/>'
            )
        if back.get("label"):
            out.append(_t(x, by + 22, back["label"], "dgm-lanelabel"))
            height = by + 28 - y
        else:
            height = by + 8 - y

    cap, cap_extra = _caption(spec, x, y + height + 16)
    if cap:
        out.append(cap)
        height += 20 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# pipeline — stages down the page, with the work named on the way
#
# Horizontal flow runs out of room after four boxes. A vertical pipeline can
# carry ten stages and still name what happens between each pair, which is
# what data-preparation and compiler pictures actually need.
# --------------------------------------------------------------------------

def _vis_pipeline(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    stages = spec.get("stages", [])
    if not stages:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    bh = 42
    out: list[str] = []
    cy = y

    for i, stage in enumerate(stages):
        via = stage.get("via")
        if i:
            via_lines = _wrap_text(via, w - 90, 12.5) if via else []
            step_h = max(30, len(via_lines) * 16 + 14)
            mid = x + 26
            out.append(
                f'<line x1="{mid:.0f}" y1="{cy:.0f}" x2="{mid:.0f}" '
                f'y2="{cy + step_h - 6:.0f}" class="dgm-arrow" '
                f'marker-end="url(#dgm-head)"/>'
            )
            for j, line in enumerate(via_lines):
                out.append(_t(mid + 14, cy + 14 + j * 16, line, "dgm-via"))
            cy += step_h

        tone = _tone(stage)
        out.append(
            f'<rect x="{x:.0f}" y="{cy:.0f}" width="{w:.0f}" height="{bh}" '
            f'rx="5" class="{_cls("dgm-band", tone)}"/>'
        )
        out.append(_t(x + 16, cy + bh / 2 + 5, stage.get("text", ""),
                      _cls("dgm-bandtext", tone)))
        if stage.get("note"):
            out.append(_t(x + w - 16, cy + bh / 2 + 5, stage["note"],
                          "dgm-bandnote", "end"))
        cy += bh

    height = cy - y
    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# mapping — in, out, and a verdict
#
# Rows of "this goes in, that comes out", with a tick or a cross where the
# point is that one of them worked and the other did not. Prompting, tokenising
# and failure-mode entries are all this shape.
# --------------------------------------------------------------------------

def _check(cx: float, cy: float, tone: str) -> str:
    if tone == "bad":
        return (
            f'<g class="dgm-verdict dgm-verdict--bad">'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9"/>'
            f'<path d="M {cx - 4:.0f} {cy - 4:.0f} L {cx + 4:.0f} {cy + 4:.0f} '
            f'M {cx + 4:.0f} {cy - 4:.0f} L {cx - 4:.0f} {cy + 4:.0f}"/></g>'
        )
    return (
        f'<g class="dgm-verdict dgm-verdict--ok">'
        f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9"/>'
        f'<path d="M {cx - 4.5:.0f} {cy:.0f} L {cx - 1:.0f} {cy + 3.5:.0f} '
        f'L {cx + 5:.0f} {cy - 4:.0f}"/></g>'
    )


def _vis_mapping(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    rows = spec.get("rows", [])
    if not rows:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    has_mark = any(r.get("mark") for r in rows)
    mark_w = 30 if has_mark else 0
    arrow_w = 44
    col_w = (w - arrow_w - mark_w) / 2
    out: list[str] = []
    cy = y

    head = spec.get("head")
    if head:
        out.append(_t(x + 14, cy + 12, head[0], "dgm-thead"))
        if len(head) > 1:
            out.append(_t(x + col_w + arrow_w + 14, cy + 12, head[1], "dgm-thead"))
        cy += 24

    for row in rows:
        left_lines = _wrap_text(row.get("left", ""), col_w - 28, 13, mono=True)
        right_lines = _wrap_text(row.get("right", ""), col_w - 28, 13, mono=True)
        lines = max(len(left_lines), len(right_lines), 1)
        rh = max(42, lines * 19 + 22)
        tone = _tone(row)
        mark = row.get("mark")

        out.append(
            f'<rect x="{x:.0f}" y="{cy:.0f}" width="{col_w:.0f}" height="{rh:.0f}" '
            f'rx="5" class="dgm-mapcell"/>'
        )
        out.append(
            f'<rect x="{x + col_w + arrow_w:.0f}" y="{cy:.0f}" width="{col_w:.0f}" '
            f'height="{rh:.0f}" rx="5" '
            f'class="{_cls("dgm-mapcell", tone or ("ok" if mark == "ok" else "bad" if mark == "bad" else ""))}"/>'
        )
        ty = cy + rh / 2 - (lines - 1) * 9.5 + 5
        out.append(_text_block(x + 14, ty, left_lines, "dgm-maptext", 19))
        out.append(_text_block(x + col_w + arrow_w + 14, ty, right_lines,
                               _cls("dgm-maptext", tone), 19))
        out.append(_arrow(x + col_w + 12, cy + rh / 2, x + col_w + arrow_w - 12))
        if mark:
            out.append(_check(x + w - 12, cy + rh / 2, "bad" if mark == "bad" else "ok"))
        if row.get("note"):
            cy += rh + 4
            out.append(_t(x + 14, cy + 12, row["note"], "dgm-caption"))
            cy += 18
        else:
            cy += rh + 10

    height = cy - y - 10
    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# matrix — a field of weights
#
# Cell opacity carries the number, so the pattern is visible before any digit
# is read. Attention maps, confusion matrices, routing tables.
# --------------------------------------------------------------------------

def _vis_matrix(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    rows = spec.get("rows", [])
    cols = spec.get("cols", [])
    if not rows:
        return "", 0.0
    label_w = max((_w_mono(r.get("label", "")) for r in rows), default=0)
    cw = float(spec.get("cell_width", 74))
    ch = 38
    grid_x = x + label_w + LABEL_GAP
    out: list[str] = []
    cy = y

    if cols:
        for j, col in enumerate(cols):
            out.append(_t(grid_x + j * cw + cw / 2, cy + 12, col, "dgm-matcol", "middle"))
        cy += 22

    show = bool(spec.get("show_values", True))
    for row in rows:
        if row.get("label"):
            out.append(_t(grid_x - LABEL_GAP, cy + ch / 2 + 5, row["label"],
                          _cls("dgm-rowlabel", _tone(row)), "end"))
        present = [v for v in row.get("values", []) if v is not None]
        peak = max(present or [0])
        for j, val in enumerate(row.get("values", [])):
            # `null` means the cell does not exist — a masked position, an
            # impossible pair. Drawing it as 0.00 says "we measured zero here",
            # which is a different and wrong claim.
            if val is None:
                continue
            v = max(0.0, min(1.0, float(val)))
            cx = grid_x + j * cw
            top_cell = v >= peak - 1e-9
            out.append(
                f'<rect x="{cx:.1f}" y="{cy:.0f}" width="{cw - 3:.1f}" height="{ch}" '
                f'rx="3" class="dgm-matcell" fill-opacity="{0.05 + v * 0.9:.3f}"/>'
            )
            if show:
                # Reversed type only once the fill is dark enough to carry it.
                cls = "dgm-matval--hi" if v >= 0.72 else (
                    "dgm-matval--peak" if top_cell else "dgm-matval")
                out.append(_t(cx + (cw - 3) / 2, cy + ch / 2 + 4,
                              f"{v:.2f}".lstrip("0"), cls, "middle"))
        cy += ch + 4

    height = cy - y - 4
    cap, cap_extra = _caption(spec, grid_x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# scatter — meaning as position
#
# Points in a plane with named groups. For embeddings, latent spaces and any
# claim of the form "these ended up near each other".
# --------------------------------------------------------------------------

def _vis_scatter(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    groups = spec.get("groups", [])
    if not groups:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    h = float(spec.get("height", 240))
    pts = [p for g in groups for p in g.get("points", [])]
    xs = [float(p[0]) for p in pts] or [0, 1]
    ys = [float(p[1]) for p in pts] or [0, 1]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    span_x = (x1 - x0) or 1
    span_y = (y1 - y0) or 1
    x0 -= span_x * 0.12
    x1 += span_x * 0.12
    y0 -= span_y * 0.12
    y1 += span_y * 0.12
    pad = 18

    def px(v: float) -> float:
        return x + pad + (float(v) - x0) / (x1 - x0) * (w - pad * 2)

    def py(v: float) -> float:
        return y + h - pad - (float(v) - y0) / (y1 - y0) * (h - pad * 2)

    out = [
        f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
        f'rx="6" class="dgm-plane"/>'
    ]

    for link in spec.get("links", []):
        a, b = link["from"], link["to"]
        out.append(
            f'<line x1="{px(a[0]):.1f}" y1="{py(a[1]):.1f}" x2="{px(b[0]):.1f}" '
            f'y2="{py(b[1]):.1f}" class="dgm-link"/>'
        )
        if link.get("text"):
            out.append(_t(
                (px(a[0]) + px(b[0])) / 2 + float(link.get("dx", 0)),
                (py(a[1]) + py(b[1])) / 2 + float(link.get("dy", 18)),
                link["text"], "dgm-linktext", link.get("anchor", "middle")))

    for g in groups:
        tone = _tone(g)
        gp = g.get("points", [])
        for p in gp:
            out.append(
                f'<circle cx="{px(p[0]):.1f}" cy="{py(p[1]):.1f}" '
                f'r="{g.get("size", 5)}" class="{_cls("dgm-dot", tone)}"/>'
            )
        if g.get("label") and gp:
            lx = sum(px(p[0]) for p in gp) / len(gp)
            ly = min(py(p[1]) for p in gp) - 15
            out.append(_t(lx, ly, g["label"], _cls("dgm-grouplabel", tone), "middle"))

    height = h
    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# tree — one thing becoming several
#
# Top-down branching, laid out by leaf packing so subtrees never collide.
# Search beams, taxonomies, the feature hierarchy a deep network learns.
# --------------------------------------------------------------------------

TREE_NODE_W = 128
TREE_NODE_H = 38
TREE_H_GAP = 14
TREE_V_GAP = 42


def _tree_leaves(node: dict[str, Any]) -> int:
    kids = node.get("children") or []
    return sum(_tree_leaves(k) for k in kids) if kids else 1


def _tree_depth(node: dict[str, Any]) -> int:
    kids = node.get("children") or []
    return 1 + max((_tree_depth(k) for k in kids), default=0)


def _tree_place(node: dict[str, Any], left: float, depth: int,
                unit: float, out: list[str], extent: list[float]) -> float:
    span = _tree_leaves(node) * unit
    centre = left + span / 2
    ny = depth * (TREE_NODE_H + TREE_V_GAP)
    tone = _tone(node)
    nx = centre - TREE_NODE_W / 2
    kids = node.get("children") or []

    extent[0] = max(extent[0], ny + TREE_NODE_H + (20 if node.get("note") else 0))

    cursor = left
    for kid in kids:
        kid_centre = _tree_place(kid, cursor, depth + 1, unit, out, extent)
        cursor += _tree_leaves(kid) * unit
        out.append(
            f'<path d="M {centre:.1f} {ny + TREE_NODE_H:.0f} '
            f'C {centre:.1f} {ny + TREE_NODE_H + TREE_V_GAP * 0.6:.0f}, '
            f'{kid_centre:.1f} {ny + TREE_NODE_H + TREE_V_GAP * 0.4:.0f}, '
            f'{kid_centre:.1f} {ny + TREE_NODE_H + TREE_V_GAP:.0f}" '
            f'class="dgm-edge"/>'
        )

    out.append(
        f'<rect x="{nx:.1f}" y="{ny:.0f}" width="{TREE_NODE_W}" '
        f'height="{TREE_NODE_H}" rx="5" class="{_cls("dgm-node", tone)}"/>'
    )
    out.append(_t(centre, ny + TREE_NODE_H / 2 + 5, node.get("text", ""),
                  _cls("dgm-nodetext", tone), "middle"))
    if node.get("note"):
        out.append(_t(centre, ny + TREE_NODE_H + 14, node["note"], "dgm-caption", "middle"))
    return centre


def _tree_gutter(spec: dict[str, Any]) -> float:
    """Room on the left for level labels, which are drawn outside the tree."""
    levels = spec.get("levels") or []
    return (max((_w_mono(name) for name in levels), default=0) + 14) if levels else 0.0


def _vis_tree(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    root = spec.get("root")
    if not root:
        return "", 0.0
    gutter = _tree_gutter(spec)
    x += gutter
    leaves = _tree_leaves(root)
    unit = TREE_NODE_W + TREE_H_GAP
    inner: list[str] = []
    extent = [0.0]
    _tree_place(root, 0, 0, unit, inner, extent)
    width = leaves * unit
    avail = float(spec.get("width", VIS_W)) - gutter
    scale = min(1.0, avail / width) if width else 1.0
    body = "\n".join(inner)
    out = [
        f'<g transform="translate({x:.1f},{y:.0f}) scale({scale:.4f})">{body}</g>'
    ]
    height = extent[0] * scale
    if spec.get("levels"):
        for i, label in enumerate(spec["levels"]):
            ly = y + (i * (TREE_NODE_H + TREE_V_GAP) + TREE_NODE_H / 2 + 5) * scale
            out.append(_t(x - 12, ly, label, "dgm-rowlabel", "end"))
    cap, cap_extra = _caption(spec, x - gutter, y + height + 20)
    if cap:
        out.append(cap)
        height += 24 + cap_extra
    return "\n".join(out), height


# --------------------------------------------------------------------------
# lineage — what came from what
#
# A rail of milestones. This is the Evolution section's shape: a chain of
# named steps where the only extra information is which one you are standing on.
# --------------------------------------------------------------------------

def _vis_lineage(spec: dict[str, Any], x: float, y: float) -> tuple[str, float]:
    items = spec.get("milestones", [])
    if not items:
        return "", 0.0
    w = float(spec.get("width", VIS_W))
    per_row = int(spec.get("per_row", 4))
    rows = [items[i:i + per_row] for i in range(0, len(items), per_row)]
    out: list[str] = []
    cy = y
    bh = 46

    for r, row in enumerate(rows):
        n = len(row)
        gap = 30
        bw = (w - gap * (per_row - 1)) / per_row
        for i, item in enumerate(row):
            tone = _tone(item)
            bx = x + i * (bw + gap)
            text = item.get("text", "") if isinstance(item, dict) else str(item)
            out.append(
                f'<rect x="{bx:.1f}" y="{cy:.0f}" width="{bw:.1f}" height="{bh}" '
                f'rx="23" class="{_cls("dgm-pill", tone)}"/>'
            )
            out.append(_t(bx + bw / 2, cy + bh / 2 + 5, text,
                          _cls("dgm-pilltext", tone), "middle"))
            if isinstance(item, dict) and item.get("note"):
                out.append(_t(bx + bw / 2, cy + bh + 16, item["note"],
                              "dgm-caption", "middle"))
            last_in_row = i == n - 1
            if not last_in_row:
                out.append(_arrow(bx + bw + 6, cy + bh / 2, bx + bw + gap - 7))
        note_pad = 20 if any(isinstance(i, dict) and i.get("note") for i in row) else 0
        cy += bh + note_pad
        if r < len(rows) - 1:
            out.append(_t(x + w / 2, cy + 18, "↓", "dgm-caption", "middle"))
            cy += 30

    height = cy - y
    cap, cap_extra = _caption(spec, x, y + height + 18)
    if cap:
        out.append(cap)
        height += 22 + cap_extra
    return "\n".join(out), height


VISUALS = {
    "grid": _vis_grid,
    "bars": _vis_bars,
    "fan": _vis_fan,
    "chips": _vis_chips,
    "stack": _vis_stack,
    "columns": _vis_columns,
    "table": _vis_table,
    "segments": _vis_segments,
    "plot": _vis_plot,
    "passes": _vis_passes,
    "pipeline": _vis_pipeline,
    "mapping": _vis_mapping,
    "matrix": _vis_matrix,
    "scatter": _vis_scatter,
    "tree": _vis_tree,
    "lineage": _vis_lineage,
}


def _render_visual(spec: dict[str, Any] | None, x: float, y: float) -> tuple[str, float]:
    if not spec:
        return "", 0.0
    fn = VISUALS.get(spec.get("kind", ""))
    return fn(spec, x, y) if fn else ("", 0.0)


# --------------------------------------------------------------------------
# note wrapping
# --------------------------------------------------------------------------

def _fit_notes(notes: list[Any], available: float) -> list[Any]:
    out: list[Any] = []
    for note in notes:
        if isinstance(note, dict):
            lead, rest = note.get("label", ""), note.get("text", "")
            budget = available - (len(lead) * SANS_ADV + 12)
        else:
            lead, rest, budget = None, str(note), available
        line, lines = "", []
        for word in rest.split():
            candidate = (line + " " + word).strip()
            if len(candidate) * SANS_ADV > budget and line:
                lines.append(line)
                line = word
                budget = available
            else:
                line = candidate
        if line:
            lines.append(line)
        for i, text in enumerate(lines):
            out.append({"label": lead, "text": text} if i == 0 and lead is not None else text)
    return out


# --------------------------------------------------------------------------
# layouts
# --------------------------------------------------------------------------


def _footer(spec: dict[str, Any], y: float) -> tuple[str, float]:
    """The closing line, wrapped.

    It used to be emitted as a single unbroken run, so any footer longer than
    the canvas simply left the frame — invisible in the spec, invisible in
    review, and clipped on the page.
    """
    text = spec.get("footer")
    if not text:
        return "", 0.0
    width = W - PAD * 2 - 8
    lines = []
    line = ""
    for word in str(text).split():
        candidate = (line + " " + word).strip()
        if len(candidate) * FOOTER_ADV > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    markup = _text_block(PAD + 4, y, lines, "dgm-footer", FOOTER_LEAD)
    return markup, (len(lines) - 1) * FOOTER_LEAD


def _render_steps(spec: dict[str, Any]) -> str:
    """Stacked layout: a compact caption, then the picture at full width.

    The earlier side-by-side version gave the prose sixty per cent of every
    panel, so the eye read text and skipped the figure. Here the visual leads
    and the words caption it -- which is the correct order for a diagram.
    """
    steps = spec.get("steps", [])
    body: list[str] = []
    y = PAD
    inner_w = W - PAD * 2

    for i, step in enumerate(steps, start=1):
        notes = _fit_notes(step.get("notes", []), inner_w - TITLE_X - STEP_PAD * 2)
        vis_spec = step.get("visual")

        head_h = 26 + len(notes) * NOTE_LEAD
        # Measure the visual once to centre it, then render at the real offset.
        probe, vis_h = _render_visual(vis_spec, 0, 0)
        vis_w = _visual_width(vis_spec)
        vis_x = PAD + (inner_w - vis_w) / 2
        vis_markup, vis_h = _render_visual(
            vis_spec, vis_x, y + STEP_PAD + head_h + (14 if vis_h else 0)
        )
        height = STEP_PAD * 2 + head_h + (vis_h + 20 if vis_h else 0)

        body.append(f'<g class="dgm-step" style="--i:{i - 1}">')
        body.append(
            f'<rect x="{PAD}" y="{y:.0f}" width="{inner_w}" height="{height:.0f}" '
            f'rx="8" class="dgm-panel"/>'
        )
        body.append(_t(NUM_X, y + STEP_PAD + 18, f"{i:02d}", "dgm-num"))
        body.append(_t(TITLE_X, y + STEP_PAD + 18, step.get("title", ""), "dgm-title"))

        ny = y + STEP_PAD + 18 + NOTE_LEAD + 2
        for note in notes:
            if isinstance(note, dict):
                body.append(
                    f'<text x="{TITLE_X}" y="{ny:.0f}" class="dgm-note">'
                    f'<tspan class="dgm-notelabel">{escape(note["label"])}</tspan>'
                    f'<tspan dx="7">{escape(note["text"])}</tspan></text>'
                )
            else:
                body.append(_t(TITLE_X, ny, note, "dgm-note"))
            ny += NOTE_LEAD

        if vis_markup:
            body.append(vis_markup)
        body.append("</g>")
        y += height + STEP_GAP

    y -= STEP_GAP
    if spec.get("footer"):
        y += 28
        markup, extra = _footer(spec, y)
        body.append(markup)
        y += extra
    return _wrap(body, y + PAD, spec)


def _visual_width(spec: dict[str, Any] | None) -> float:
    """How much horizontal room a visual actually needs, so it can be centred."""
    if not spec:
        return 0.0
    kind = spec.get("kind")
    if kind == "grid":
        rows = spec.get("rows", [])
        label_w = max((len(str(r.get("label", ""))) * MONO_ADV for r in rows), default=0)
        cells = max((len(r.get("cells", [])) for r in rows), default=0)
        return label_w + LABEL_GAP + cells * CELL_W + max(cells - 1, 0) * CELL_GAP
    if kind == "bars":
        return VIS_W
    if kind == "fan":
        targets = spec.get("targets", [])
        src_w = max(68, len(str(spec.get("source", ""))) * MONO_ADV + CHIP_PAD)
        return src_w + 110 + max((_chip_w(t) for t in targets), default=78)
    if kind == "chips":
        items = spec.get("items", [])
        return sum(_chip_w(i) for i in items) + max(len(items) - 1, 0) * 12
    if kind in ("stack", "columns", "table", "segments", "plot", "passes",
                "pipeline", "mapping", "scatter", "lineage"):
        return float(spec.get("width", VIS_W))
    if kind == "matrix":
        rows = spec.get("rows", [])
        cols = spec.get("cols", [])
        ncol = max(len(cols), max((len(r.get("values", [])) for r in rows), default=0))
        label_w = max((len(str(r.get("label", ""))) * MONO_ADV for r in rows), default=0)
        return label_w + LABEL_GAP + ncol * float(spec.get("cell_width", 74))
    if kind == "tree":
        root = spec.get("root")
        if not root:
            return 0.0
        gutter = _tree_gutter(spec)
        natural = _tree_leaves(root) * (TREE_NODE_W + TREE_H_GAP)
        return min(natural + gutter, float(spec.get("width", VIS_W)))
    return 0.0


def _render_flow(spec: dict[str, Any]) -> str:
    nodes = spec.get("nodes", [])
    if not nodes:
        return ""
    body: list[str] = []
    n = len(nodes)
    gap = 34
    box_w = (W - PAD * 2 - gap * (n - 1)) / n
    note_lines = max(
        (len(_wrap_text(node.get("note", ""), box_w - 18, 12))
         for node in nodes if node.get("note")), default=1)
    box_h = 62 + (note_lines - 1) * 15
    # The return arc rides above the row. Underneath, it would have to cross the
    # per-node captions, which sit exactly where its verticals would drop.
    loop_lane = 40 if spec.get("loop") else 0
    y = PAD + 14 + loop_lane

    for i, node in enumerate(nodes):
        x = PAD + i * (box_w + gap)
        accent = bool(node.get("accent"))
        body.append(f'<g class="dgm-step" style="--i:{i}">')
        body.append(
            f'<rect x="{x:.0f}" y="{y}" width="{box_w:.0f}" height="{box_h}" rx="6" '
            f'class="{"dgm-box dgm-box--accent" if accent else "dgm-box"}"/>'
        )
        body.append(_t(x + box_w / 2, y + 26, node.get("title", ""), "dgm-boxtitle", "middle"))
        if node.get("note"):
            body.append(_text_block(x + box_w / 2, y + 45,
                                    _wrap_text(node["note"], box_w - 18, 12, mono=True),
                                    "dgm-boxnote", 15, "middle"))
        if node.get("caption"):
            body.append(_text_block(x + box_w / 2, y + box_h + 22,
                                    _wrap_text(node["caption"], box_w + gap - 8, 12.5),
                                    "dgm-caption", CAP_LEAD, "middle"))
        if i < n - 1:
            body.append(_arrow(x + box_w + 6, y + box_h / 2, x + box_w + gap - 8))
        body.append("</g>")

    cap_lines = max((len(_wrap_text(node.get("caption", ""), box_w + gap - 8, 12.5))
                     for node in nodes if node.get("caption")), default=0)
    height = y + box_h + (26 + (cap_lines - 1) * CAP_LEAD if cap_lines else 0) + PAD
    if spec.get("loop"):
        ly = PAD + 6
        x1 = PAD + (n - 1) * (box_w + gap) + box_w / 2
        x2 = PAD + box_w / 2
        body.append(
            f'<path d="M {x1:.0f} {y:.0f} L {x1:.0f} {ly:.0f} L {x2:.0f} {ly:.0f} '
            f'L {x2:.0f} {y - 8:.0f}" class="dgm-arrow dgm-arrow--loop" '
            f'marker-end="url(#dgm-head)"/>'
        )
        body.append(_t((x1 + x2) / 2, ly - 8, spec["loop"], "dgm-caption", "middle"))
    if spec.get("footer"):
        height += 22
        markup, extra = _footer(spec, height - PAD)
        body.append(markup)
        height += extra
    return _wrap(body, height, spec)


def _wrap(body: list[str], height: float, spec: dict[str, Any]) -> str:
    title = spec.get("title")
    head, offset = "", 0
    if title:
        offset = 30
        head = _t(PAD, 22, title, "dgm-figtitle")
    inner = "\n".join(body)
    if offset:
        inner = f'<g transform="translate(0,{offset})">{inner}</g>'
    return (
        f'<svg class="dgm" viewBox="0 0 {W} {height + offset:.0f}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{escape(title or "Process diagram")}">'
        f'<defs><marker id="dgm-head" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 9 5 L 0 9 z" class="dgm-head"/></marker></defs>'
        f"{head}{inner}</svg>"
    )


def _render_figure(spec: dict[str, Any]) -> str:
    """A single visual with no step scaffolding — for diagrams that are one
    picture rather than a sequence."""
    vis = spec.get("visual")
    width = _visual_width(vis)
    x = PAD + (W - PAD * 2 - width) / 2
    markup, height = _render_visual(vis, x, PAD)
    body = [markup]
    total = PAD + height
    if spec.get("footer"):
        total += 28
        markup, extra = _footer(spec, total)
        body.append(markup)
        total += extra
    return _wrap(body, total + PAD, spec)


# --------------------------------------------------------------------------
# the contract
#
# One table, read by the validator, so a typo in a spec is caught at `enc
# validate` rather than discovered as a blank space on a built page. Adding a
# primitive means adding its row here; there is nowhere else to forget.
# --------------------------------------------------------------------------

COMMON_VISUAL_KEYS = {"kind", "caption", "width"}

VISUAL_KEYS: dict[str, tuple[set[str], set[str]]] = {
    "grid":     ({"rows"}, set()),
    "bars":     ({"bars"}, set()),
    "fan":      ({"source", "targets"}, set()),
    "chips":    ({"items"}, {"loop"}),
    "stack":    ({"layers"}, set()),
    "columns":  ({"columns"}, set()),
    "table":    ({"rows"}, {"head"}),
    "segments": ({"segments"}, {"label", "spans"}),
    "plot":     ({"curves"}, {"x_range", "y_range", "x_label", "y_label",
                              "height", "marks", "bands"}),
    "passes":   ({"nodes"}, {"forward", "backward"}),
    "pipeline": ({"stages"}, set()),
    "mapping":  ({"rows"}, {"head"}),
    "matrix":   ({"rows"}, {"cols", "cell_width", "show_values"}),
    "scatter":  ({"groups"}, {"height", "links"}),
    "tree":     ({"root"}, {"levels"}),
    "lineage":  ({"milestones"}, {"per_row"}),
}

LAYOUT_KEYS: dict[str, tuple[set[str], set[str]]] = {
    "steps":  ({"steps"}, {"kind", "title", "footer", "section"}),
    "flow":   ({"nodes"}, {"kind", "title", "footer", "section", "loop"}),
    "figure": ({"visual"}, {"kind", "title", "footer", "section"}),
}


def visual_issues(spec: dict[str, Any], where: str) -> list[str]:
    """Structural problems with one visual spec, in reading order."""
    kind = spec.get("kind")
    if kind not in VISUAL_KEYS:
        known = ", ".join(sorted(VISUAL_KEYS))
        return [f"{where}: unknown visual kind {kind!r} (expected one of: {known})"]
    required, optional = VISUAL_KEYS[kind]
    allowed = required | optional | COMMON_VISUAL_KEYS
    out = [
        f"{where}: {kind} visual is missing required key {key!r}"
        for key in sorted(required - set(spec))
    ]
    out += [
        f"{where}: {kind} visual has no key {key!r} "
        f"(allowed: {', '.join(sorted(allowed))})"
        for key in sorted(set(spec) - allowed)
    ]
    return out


def _is_accented(item: Any) -> bool:
    return isinstance(item, dict) and bool(
        item.get("accent") or item.get("new") or item.get("tone") == "accent"
    )


def _accent_noise(node: Any) -> int:
    """The largest number of accents in any one list that also has an unmarked
    member.

    Counting accents outright gets this wrong: a prefill grid marks all eight
    cells because at prefill all eight really are new, and that is one statement,
    not eight. The accent only stops meaning anything when it is applied to most
    of a set but not all of it — so that is what this looks for.
    """
    worst = 0
    if isinstance(node, list):
        marked = sum(1 for item in node if _is_accented(item))
        if marked and marked < len(node):
            worst = marked
        for item in node:
            worst = max(worst, _accent_noise(item))
    elif isinstance(node, dict):
        for value in node.values():
            worst = max(worst, _accent_noise(value))
    return worst


def diagram_issues(spec: dict[str, Any], where: str) -> tuple[list[str], list[str]]:
    """(errors, warnings) for one whole diagram."""
    errors: list[str] = []
    warnings: list[str] = []
    kind = spec.get("kind")
    if kind not in LAYOUT_KEYS:
        known = ", ".join(sorted(LAYOUT_KEYS))
        return ([f"{where}: unknown diagram kind {kind!r} (expected one of: {known})"], [])

    required, optional = LAYOUT_KEYS[kind]
    for key in sorted(required - set(spec)):
        errors.append(f"{where}: {kind} diagram is missing required key {key!r}")
    for key in sorted(set(spec) - required - optional):
        errors.append(f"{where}: {kind} diagram has no key {key!r}")

    if kind == "steps":
        for i, step in enumerate(spec.get("steps", []), start=1):
            if not isinstance(step, dict):
                errors.append(f"{where}: step {i} is not a mapping")
                continue
            for key in sorted(set(step) - {"title", "notes", "visual"}):
                errors.append(f"{where}: step {i} has no key {key!r}")
            if not step.get("title"):
                errors.append(f"{where}: step {i} is missing 'title'")
            if step.get("visual"):
                errors += visual_issues(step["visual"], f"{where}: step {i}")
            else:
                warnings.append(
                    f"{where}: step {i} has no visual — a step without a picture "
                    f"is prose in a box"
                )
    elif kind == "figure":
        if isinstance(spec.get("visual"), dict):
            errors += visual_issues(spec["visual"], where)
    elif kind == "flow":
        for i, node in enumerate(spec.get("nodes", []), start=1):
            if isinstance(node, dict):
                for key in sorted(set(node) - {"title", "note", "caption", "accent", "tone"}):
                    errors.append(f"{where}: node {i} has no key {key!r}")

    worst = _accent_noise(spec)
    if worst > 5:
        warnings.append(
            f"{where}: {worst} items in one row or list are accented while others "
            f"are not — at that density the accent no longer distinguishes anything"
        )
    return errors, warnings


def render(spec: dict[str, Any]) -> str:
    kind = spec.get("kind")
    if kind == "steps":
        return _render_steps(spec)
    if kind == "flow":
        return _render_flow(spec)
    if kind == "figure":
        return _render_figure(spec)
    return ""
