# Use Rectangle for T_NOTE head, final locked-in version
import math
from drawsvg import Drawing, Filter, FilterItem, Group, Text, Rectangle, Path, Ellipse

# --- Configuration ---
WIDTH = 400
HEIGHT = 400
BG_COLOR = '#000000' # Black background
FONT_FAMILY = "DejaVu Sans, Arial, sans-serif" # Use a font that has ℝ
APPLY_GLITCH_FILTER = True # Set True for final output, False for shape editing

# --- R Element Configuration ---
LETTER_R_COLOR = '#DFFF00' # Chartreuse Yellow
R_FONT_SIZE = 200
R_CHAR_BLACKBOARD = '\u211d' # Unicode for Blackboard Bold R

# --- T_NOTE Element Configuration ---
LETTER_T_COLOR = '#E68FAC' # Pinkish T_NOTE Fill Color
T_NOTE_SCALE = 1
T_NOTE_X_OFFSET = R_FONT_SIZE * 0.46 # Base X position relative to R center
T_NOTE_Y_OFFSET_BASE = -(R_FONT_SIZE * 0.35) # Base Y before adjustments
T_NOTE_GLOBAL_Y_OFFSET = -15 # Shifts entire T_NOTE up/down
T_NOTE_STROKE_WIDTH = 1 if not APPLY_GLITCH_FILTER else 0 # No stroke when glitched
T_NOTE_STROKE_COLOR = 'black'
T_NOTE_FILL_COLOR = LETTER_T_COLOR

# --- T_NOTE Sub-Shape Parameters ---
# Head
HEAD_RECT_WIDTH = 25 * T_NOTE_SCALE
HEAD_HEIGHT = 20 * T_NOTE_SCALE
# Claw
CLAW_TOP_CP_DX = 30 * T_NOTE_SCALE
CLAW_TOP_CP_DY = 5 * T_NOTE_SCALE
CLAW_TIP_DX = 35 * T_NOTE_SCALE
CLAW_TIP_DY = HEAD_HEIGHT/2 + (10 * T_NOTE_SCALE)
CLAW_BOT_CP_DX = 30 * T_NOTE_SCALE
CLAW_BOT_CP_DY = 0
# Handle
HANDLE_WIDTH = 20 * T_NOTE_SCALE
HANDLE_LENGTH = 60 * T_NOTE_SCALE
HANDLE_SKEW_OFFSET = -10 * T_NOTE_SCALE
HANDLE_VERTICAL_OFFSET = 15 * T_NOTE_SCALE # Gap between head and handle
HANDLE_HORIZONTAL_OFFSET = 10 # Shift handle left/right
# Back Shape
BACK_SHAPE_WIDTH = 8 * T_NOTE_SCALE
# Bottom Oval
OVAL_ROTATION_DEGREE = -10
OVAL_HORIZONTAL_OFFSET = -11 # Shift oval left/right independently
BOTTOM_ELLIPSE_RX = HANDLE_WIDTH * 1.1
BOTTOM_ELLIPSE_RY = 15 * T_NOTE_SCALE
BOTTOM_ELLIPSE_Y_OFFSET = 5 * T_NOTE_SCALE # Gap below handle

# --- Outer Ellipse Grid Parameters ---
GRID_CENTER_X = 28 # Center offset for the grid ellipses
GRID_CENTER_Y = 0
OUTER_ELLIPSE_RX = 168
OUTER_ELLIPSE_RY = 100
OUTER_ELLIPSE_STROKE_COLOR = '#111111' # Dark gray base for grid
OUTER_ELLIPSE_STROKE_WIDTH = 6
GRID_INNER_COUNT = 25 # Number of inner ellipses
GRID_OUTER_COUNT = 10 # Number of outer ellipses
GRID_INNER_SCALE_FACTOR = 0.9
GRID_OUTER_SCALE_FACTOR = 1.1
GRID_INNER_COLOR_FADE = 0.95
GRID_OUTER_COLOR_FADE = 1.07


# --- Glitch Effect Configuration ---
# Shared Glitch Colors
GLITCH_COLOR_1 = '#EE00EE' # User selected Magenta
GLITCH_COLOR_2 = '#7FFF00' # User selected Lime Green
# R Glitch Parameters
GLITCH_OFFSET_R = 6
GLITCH_FREQ_R = '0.01 0.9'
GLITCH_OCTAVES_R = '2'
GLITCH_TURBULENCE_TYPE_R = 'fractalNoise'
GLITCH_SCALE_R = '10'
GLITCH_COLOR_1_R = GLITCH_COLOR_1
GLITCH_COLOR_2_R = GLITCH_COLOR_2
# T_NOTE Glitch Parameters
GLITCH_OFFSET_T = 7
GLITCH_FREQ_T = '0.01 0.9'
GLITCH_OCTAVES_T = '1'
GLITCH_TURBULENCE_TYPE_T = 'fractalNoise'
GLITCH_SCALE_T = '1'
GLITCH_COLOR_1_T = GLITCH_COLOR_1
GLITCH_COLOR_2_T = GLITCH_COLOR_2


# --- Create Drawing ---
dwg = Drawing(WIDTH, HEIGHT, origin='center')

# --- Add Background Rectangle ---
dwg.append(Rectangle(-WIDTH/2, -HEIGHT/2, WIDTH, HEIGHT, fill=BG_COLOR))

# --- Add Outer Ellipse Grid ---
space_time_grid = Group(id='space-time-grid')
try: # Safely parse base grid color
    r_base = int(OUTER_ELLIPSE_STROKE_COLOR[1:3], 16); g_base = int(OUTER_ELLIPSE_STROKE_COLOR[3:5], 16); b_base = int(OUTER_ELLIPSE_STROKE_COLOR[5:7], 16)
except (IndexError, ValueError):
    print(f"Warning: Invalid hex color '{OUTER_ELLIPSE_STROKE_COLOR}'. Using default gray.")
    r_base, g_base, b_base = 17, 17, 17 # Default #111111
space_time_grid.append(Ellipse(GRID_CENTER_X, GRID_CENTER_Y, OUTER_ELLIPSE_RX, OUTER_ELLIPSE_RY, fill='none', stroke=OUTER_ELLIPSE_STROKE_COLOR, stroke_width=OUTER_ELLIPSE_STROKE_WIDTH))
for i in range(1, GRID_INNER_COUNT + 1): # Inner ellipses
    coeff = GRID_INNER_SCALE_FACTOR ** i; cfade = GRID_INNER_COLOR_FADE ** i
    r_in = max(0, min(255, int(r_base * cfade))); g_in = max(0, min(255, int(g_base * cfade))); b_in = max(0, min(255, int(b_base * cfade)))
    stroke_color = f"#{r_in:02x}{g_in:02x}{b_in:02x}"
    space_time_grid.append(Ellipse(GRID_CENTER_X, GRID_CENTER_Y, OUTER_ELLIPSE_RX * coeff, OUTER_ELLIPSE_RY * coeff, fill='none', stroke=stroke_color, stroke_width= OUTER_ELLIPSE_STROKE_WIDTH * coeff))
for i in range(1, GRID_OUTER_COUNT + 1): # Outer ellipses
    coeff = GRID_OUTER_SCALE_FACTOR ** i; cfade = GRID_OUTER_COLOR_FADE ** i
    r_out = max(0, min(255, int(r_base * cfade))); g_out = max(0, min(255, int(g_base * cfade))); b_out = max(0, min(255, int(b_base * cfade)))
    stroke_color = f"#{r_out:02x}{g_out:02x}{b_out:02x}"
    space_time_grid.append(Ellipse(GRID_CENTER_X, GRID_CENTER_Y, OUTER_ELLIPSE_RX * coeff, OUTER_ELLIPSE_RY * coeff, fill='none', stroke=stroke_color, stroke_width= OUTER_ELLIPSE_STROKE_WIDTH * coeff))
dwg.append(space_time_grid)

# --- Define Glitch Filter for R ---
f_r = Filter(id='glitch_r')
f_r.append(FilterItem('feTurbulence', type=GLITCH_TURBULENCE_TYPE_R, baseFrequency=GLITCH_FREQ_R, numOctaves=GLITCH_OCTAVES_R, result='turbulence_r'))
f_r.append(FilterItem('feDisplacementMap', in_='SourceGraphic', in2='turbulence_r', scale=GLITCH_SCALE_R, xChannelSelector='R', yChannelSelector='G', result='displaced_base_r'))
f_r.append(FilterItem('feOffset', in_='displaced_base_r', dx=f'-{GLITCH_OFFSET_R}', dy='0', result='offset_geom1_r'))
f_r.append(FilterItem('feOffset', in_='displaced_base_r', dx=f'{GLITCH_OFFSET_R}', dy='0', result='offset_geom2_r'))
f_r.append(FilterItem('feFlood', result='flood1_r', flood_color=GLITCH_COLOR_1_R, flood_opacity='1'))
f_r.append(FilterItem('feFlood', result='flood2_r', flood_color=GLITCH_COLOR_2_R, flood_opacity='1'))
f_r.append(FilterItem('feComposite', in_='flood1_r', in2='offset_geom1_r', operator='in', result='layer1_r'))
f_r.append(FilterItem('feComposite', in_='flood2_r', in2='offset_geom2_r', operator='in', result='layer2_r'))
merge_r = FilterItem('feMerge'); f_r.append(merge_r)
merge_r.append(FilterItem('feMergeNode', in_='layer1_r')); merge_r.append(FilterItem('feMergeNode', in_='layer2_r')); merge_r.append(FilterItem('feMergeNode', in_='displaced_base_r'))

# --- Define Glitch Filter for T_NOTE ---
f_t = Filter(id='glitch_t')
f_t.append(FilterItem('feTurbulence', type=GLITCH_TURBULENCE_TYPE_T, baseFrequency=GLITCH_FREQ_T, numOctaves=GLITCH_OCTAVES_T, result='turbulence_t'))
f_t.append(FilterItem('feDisplacementMap', in_='SourceGraphic', in2='turbulence_t', scale=GLITCH_SCALE_T, xChannelSelector='R', yChannelSelector='G', result='displaced_base_t'))
f_t.append(FilterItem('feOffset', in_='displaced_base_t', dx=f'-{GLITCH_OFFSET_T}', dy='0', result='offset_geom1_t'))
f_t.append(FilterItem('feOffset', in_='displaced_base_t', dx=f'{GLITCH_OFFSET_T}', dy='0', result='offset_geom2_t'))
f_t.append(FilterItem('feFlood', result='flood1_t', flood_color=GLITCH_COLOR_1_T, flood_opacity='1'))
f_t.append(FilterItem('feFlood', result='flood2_t', flood_color=GLITCH_COLOR_2_T, flood_opacity='1'))
f_t.append(FilterItem('feComposite', in_='flood1_t', in2='offset_geom1_t', operator='in', result='layer1_t'))
f_t.append(FilterItem('feComposite', in_='flood2_t', in2='offset_geom2_t', operator='in', result='layer2_t'))
merge_t = FilterItem('feMerge'); f_t.append(merge_t)
merge_t.append(FilterItem('feMergeNode', in_='layer1_t')); merge_t.append(FilterItem('feMergeNode', in_='layer2_t')); merge_t.append(FilterItem('feMergeNode', in_='displaced_base_t'))


# --- Create MAIN Group (contains R and T_NOTE) ---
main_logo_group = Group(font_family=FONT_FAMILY, font_weight='bold', text_anchor='middle')

# --- R Elements ---
r_group = Group(fill=LETTER_R_COLOR, filter=f_r if APPLY_GLITCH_FILTER else None)
r_y_adjust = R_FONT_SIZE * 0.1
path_fill = 'inherit' if APPLY_GLITCH_FILTER else '#CCCCCC' # Use inherit for final, gray for dev
path_top_hole = Path(stroke='none', fill=path_fill).M(15, -55).L(30, -50).L(48, -40).L(45, -5).L(10, 7).L(25, -20).Z()
path_bottom_hole = Path(stroke='none', fill=path_fill).M(-10, 5).L(15, 5).L(60, 65).L(35, 65).Z()
r_group.append(Text(R_CHAR_BLACKBOARD, font_size=R_FONT_SIZE, x=0, y=r_y_adjust, dominant_baseline='middle'))
r_group.append(path_top_hole); r_group.append(path_bottom_hole)
main_logo_group.append(r_group)

# --- T_NOTE Elements ---
t_note_final_y = T_NOTE_Y_OFFSET_BASE + r_y_adjust + T_NOTE_GLOBAL_Y_OFFSET
t_note_group = Group(transform=f'translate({T_NOTE_X_OFFSET}, {t_note_final_y})',
                     filter=f_t if APPLY_GLITCH_FILTER else None)

# Define T_NOTE parts relative to its group's origin (0,0)
head_t_y = HEAD_HEIGHT / 2; head_b_y = -HEAD_HEIGHT / 2
head_l_x = -HEAD_RECT_WIDTH / 2; head_r_x = HEAD_RECT_WIDTH / 2
handle_t_y = head_b_y + HANDLE_VERTICAL_OFFSET
handle_b_y = handle_t_y + HANDLE_LENGTH
handle_t_lx = -HANDLE_WIDTH/2 + HANDLE_HORIZONTAL_OFFSET; handle_t_rx = HANDLE_WIDTH/2 + HANDLE_HORIZONTAL_OFFSET
handle_b_lx = handle_t_lx + HANDLE_SKEW_OFFSET; handle_b_rx = handle_t_rx + HANDLE_SKEW_OFFSET
ellipse_c_x = (handle_b_lx + handle_b_rx) / 2 + OVAL_HORIZONTAL_OFFSET
ellipse_c_y = handle_b_y + BOTTOM_ELLIPSE_Y_OFFSET

# Head - Rectangular Part (Using Rectangle)
head_rect_x = head_l_x - 2
head_rect_y = head_b_y # The minimum y value is the top in this context
t_note_group.append(Rectangle(head_rect_x, head_rect_y, HEAD_RECT_WIDTH + 12.2, HEAD_HEIGHT,
                               stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH,
                               fill=T_NOTE_FILL_COLOR))

# Head - Claw Part
t_note_group.append(Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
                    .M(head_r_x + 10, head_b_y).Q(head_r_x + CLAW_TOP_CP_DX, head_b_y + CLAW_TOP_CP_DY, head_r_x + CLAW_TIP_DX, CLAW_TIP_DY)
                    .Q(head_r_x + CLAW_BOT_CP_DX, head_t_y + CLAW_BOT_CP_DY, head_r_x + 10, head_t_y).Z())
# Shape 1: Back Protrusion
back_p_A = (head_l_x, head_t_y); back_p_B = (head_l_x, head_b_y); back_p_C = (head_l_x - BACK_SHAPE_WIDTH - 6, head_b_y); back_p_D = (head_l_x - BACK_SHAPE_WIDTH + HANDLE_SKEW_OFFSET, head_t_y)
t_note_group.append(Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
                    .M(*back_p_A).L(*back_p_D).L(*back_p_C).L(*back_p_B).Z())
# Handle (Stem)
t_note_group.append(Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
                    .M(handle_t_lx, handle_t_y).L(handle_t_rx, handle_t_y).L(handle_b_rx, handle_b_y).L(handle_b_lx, handle_b_y).Z())
# Shape 2: Bottom Oval
ellipse_tf = f"rotate({OVAL_ROTATION_DEGREE}, {ellipse_c_x}, {ellipse_c_y})" if OVAL_ROTATION_DEGREE != 0 else None
t_note_group.append(Ellipse(ellipse_c_x, ellipse_c_y, BOTTOM_ELLIPSE_RX, BOTTOM_ELLIPSE_RY,
                            stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH,
                            fill=T_NOTE_FILL_COLOR, transform=ellipse_tf))

main_logo_group.append(t_note_group)

dwg.append(main_logo_group)

# --- Save the SVG ---
suffix = "final" if APPLY_GLITCH_FILTER else "shape_only"
dwg.save_svg(f'transpose_real_logo_{suffix}.svg')
print(f"SVG logo 'transpose_real_logo_{suffix}.svg' saved.")
