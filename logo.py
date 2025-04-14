# Separate Glitch Filters for R and T_NOTE
import math
from drawsvg import Drawing, Filter, FilterItem, Group, Text, Rectangle, Path, Ellipse

# --- Configuration ---
WIDTH = 400
HEIGHT = 400
BG_COLOR = '#1a1a1a'
LETTER_R_COLOR = '#DFFF00'
LETTER_T_COLOR = '#E68FAC' # T_NOTE Fill Color
FONT_FAMILY = "DejaVu Sans, Arial, sans-serif"
R_FONT_SIZE = 200
R_CHAR_BLACKBOARD = '\u211d'

# --- Toggle Glitch Filter ---
APPLY_GLITCH_FILTER = True # Keep OFF for shape iteration

# --- T_NOTE Shape Parameters (Unchanged) ---
T_NOTE_SCALE = 1
T_NOTE_X_OFFSET = R_FONT_SIZE * 0.45
T_NOTE_Y_OFFSET_BASE = -(R_FONT_SIZE * 0.35)
T_NOTE_GLOBAL_Y_OFFSET = -20
HEAD_RECT_WIDTH = 25 * T_NOTE_SCALE
HEAD_HEIGHT = 20 * T_NOTE_SCALE
CLAW_TOP_CP_DX = 30 * T_NOTE_SCALE
CLAW_TOP_CP_DY = 5 * T_NOTE_SCALE
CLAW_TIP_DX = 35 * T_NOTE_SCALE
CLAW_TIP_DY = HEAD_HEIGHT/2 + (10 * T_NOTE_SCALE)
CLAW_BOT_CP_DX = 15 * T_NOTE_SCALE
CLAW_BOT_CP_DY = -5 * T_NOTE_SCALE
HANDLE_WIDTH = 20 * T_NOTE_SCALE
HANDLE_LENGTH = 60 * T_NOTE_SCALE
HANDLE_SKEW_OFFSET = -10 * T_NOTE_SCALE
HANDLE_VERTICAL_OFFSET = 15 * T_NOTE_SCALE
HANDLE_HORIZONTAL_OFFSET = 10
BACK_SHAPE_WIDTH = 8 * T_NOTE_SCALE
OVAL_ROTATION_DEGREE = -10
OVAL_HORIZONTAL_OFFSET = -8
BOTTOM_ELLIPSE_RX = HANDLE_WIDTH * 1.1
BOTTOM_ELLIPSE_RY = 15 * T_NOTE_SCALE
BOTTOM_ELLIPSE_Y_OFFSET = 5 * T_NOTE_SCALE
T_NOTE_STROKE_WIDTH = 1 if not APPLY_GLITCH_FILTER else 0
T_NOTE_STROKE_COLOR = 'black'
T_NOTE_FILL_COLOR = LETTER_T_COLOR


# --- Glitch Effect Variables (Now Separate for R and T_NOTE) ---

# --- R Glitch Parameters ---
ABERRATION_OFFSET_R = 6
TURBULENCE_BASE_FREQ_R = '0.01 0.9'
TURBULENCE_OCTAVES_R = '2'
TURBULENCE_TYPE_R = 'fractalNoise'
DISPLACEMENT_SCALE_R = '10'
ABERRATION_COLOR_CYAN_R = '#00FFFF' # Same vibrant colors for now
ABERRATION_COLOR_RED_R = '#FF0000'

# --- T_NOTE Glitch Parameters ---
ABERRATION_OFFSET_T = 7             # Can be different from R
TURBULENCE_BASE_FREQ_T = '0.01 0.9' # Can be different from R
TURBULENCE_OCTAVES_T = '1'          # Can be different from R
TURBULENCE_TYPE_T = 'fractalNoise'  # Can be different from R
DISPLACEMENT_SCALE_T = '1'         # Can be different from R
ABERRATION_COLOR_CYAN_T = '#00FFFF' # Can be different from R
ABERRATION_COLOR_RED_T = '#FF0000'  # Can be different from R


# --- Create Drawing ---
dwg = Drawing(WIDTH, HEIGHT, origin='center')

# --- Define Glitch Filter for R ---
f_r = Filter(id='glitch_r') # Unique ID
f_r.append(FilterItem('feTurbulence', type=TURBULENCE_TYPE_R, baseFrequency=TURBULENCE_BASE_FREQ_R, numOctaves=TURBULENCE_OCTAVES_R, result='turbulence_r'))
f_r.append(FilterItem('feDisplacementMap', in_='SourceGraphic', in2='turbulence_r', scale=DISPLACEMENT_SCALE_R, xChannelSelector='R', yChannelSelector='G', result='displaced_base_r'))
f_r.append(FilterItem('feOffset', in_='displaced_base_r', dx=f'-{ABERRATION_OFFSET_R}', dy='0', result='offset_cyan_geometry_r'))
f_r.append(FilterItem('feOffset', in_='displaced_base_r', dx=f'{ABERRATION_OFFSET_R}', dy='0', result='offset_red_geometry_r'))
f_r.append(FilterItem('feFlood', result='cyan_flood_color_r', flood_color=ABERRATION_COLOR_CYAN_R, flood_opacity='1'))
f_r.append(FilterItem('feFlood', result='red_flood_color_r', flood_color=ABERRATION_COLOR_RED_R, flood_opacity='1'))
f_r.append(FilterItem('feComposite', in_='cyan_flood_color_r', in2='offset_cyan_geometry_r', operator='in', result='cyan_layer_final_r'))
f_r.append(FilterItem('feComposite', in_='red_flood_color_r', in2='offset_red_geometry_r', operator='in', result='red_layer_final_r'))
merge_r = FilterItem('feMerge')
f_r.append(merge_r)
merge_r.append(FilterItem('feMergeNode', in_='cyan_layer_final_r'))
merge_r.append(FilterItem('feMergeNode', in_='red_layer_final_r'))
merge_r.append(FilterItem('feMergeNode', in_='displaced_base_r'))

# --- Define Glitch Filter for T_NOTE ---
f_t = Filter(id='glitch_t') # Unique ID
f_t.append(FilterItem('feTurbulence', type=TURBULENCE_TYPE_T, baseFrequency=TURBULENCE_BASE_FREQ_T, numOctaves=TURBULENCE_OCTAVES_T, result='turbulence_t'))
f_t.append(FilterItem('feDisplacementMap', in_='SourceGraphic', in2='turbulence_t', scale=DISPLACEMENT_SCALE_T, xChannelSelector='R', yChannelSelector='G', result='displaced_base_t'))
f_t.append(FilterItem('feOffset', in_='displaced_base_t', dx=f'-{ABERRATION_OFFSET_T}', dy='0', result='offset_cyan_geometry_t'))
f_t.append(FilterItem('feOffset', in_='displaced_base_t', dx=f'{ABERRATION_OFFSET_T}', dy='0', result='offset_red_geometry_t'))
f_t.append(FilterItem('feFlood', result='cyan_flood_color_t', flood_color=ABERRATION_COLOR_CYAN_T, flood_opacity='1'))
f_t.append(FilterItem('feFlood', result='red_flood_color_t', flood_color=ABERRATION_COLOR_RED_T, flood_opacity='1'))
f_t.append(FilterItem('feComposite', in_='cyan_flood_color_t', in2='offset_cyan_geometry_t', operator='in', result='cyan_layer_final_t'))
f_t.append(FilterItem('feComposite', in_='red_flood_color_t', in2='offset_red_geometry_t', operator='in', result='red_layer_final_t'))
merge_t = FilterItem('feMerge')
f_t.append(merge_t)
merge_t.append(FilterItem('feMergeNode', in_='cyan_layer_final_t'))
merge_t.append(FilterItem('feMergeNode', in_='red_layer_final_t'))
merge_t.append(FilterItem('feMergeNode', in_='displaced_base_t'))


# --- Create MAIN Group (contains R and T_NOTE) ---
main_group = Group(
    font_family=FONT_FAMILY,
    font_weight='bold',
    text_anchor='middle',
    # Filter removed from main group
)

# --- R Elements ---
# Apply filter f_r conditionally to r_group
r_group = Group(
    fill=LETTER_R_COLOR,
    filter=f_r if APPLY_GLITCH_FILTER else None
)
r_y_adjust = R_FONT_SIZE * 0.1
# Conditional fill for paths now relies on the main APPLY_GLITCH_FILTER flag
path_top_hole = Path(stroke='none', fill='inherit' if APPLY_GLITCH_FILTER else '#CCCCCC').M(15, -55).L(30, -50).L(48, -40).L(45, -5).L(10, 7).L(25, -20).Z() # Changed dev fill
path_bottom_hole = Path(stroke='none', fill='inherit' if APPLY_GLITCH_FILTER else '#CCCCCC').M(-10, 5).L(15, 5).L(60, 65).L(35, 65).Z() # Changed dev fill
r_group.append(Text(R_CHAR_BLACKBOARD, font_size=R_FONT_SIZE, x=0, y=r_y_adjust, dominant_baseline='middle'))
r_group.append(path_top_hole)
r_group.append(path_bottom_hole)
main_group.append(r_group)

# --- T_NOTE Elements ---
t_note_final_y_offset = T_NOTE_Y_OFFSET_BASE + r_y_adjust + T_NOTE_GLOBAL_Y_OFFSET
# Apply filter f_t conditionally to t_note_group
t_note_group = Group(
    transform=f'translate({T_NOTE_X_OFFSET}, {t_note_final_y_offset})',
    filter=f_t if APPLY_GLITCH_FILTER else None
)

# Coordinates relative to t_note_group origin
head_top_y = HEAD_HEIGHT / 2
head_bottom_y = -HEAD_HEIGHT / 2
head_rect_left_x = -HEAD_RECT_WIDTH / 2
head_rect_right_x = HEAD_RECT_WIDTH / 2

# Head - Rectangular Part
head_rect = Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
head_rect.M(head_rect_left_x, head_top_y).L(head_rect_right_x, head_top_y).L(head_rect_right_x, head_bottom_y).L(head_rect_left_x, head_bottom_y).Z()
t_note_group.append(head_rect)

# Head - Claw Part
claw_part = Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
claw_start_x = head_rect_right_x
claw_part.M(claw_start_x, head_bottom_y).Q(claw_start_x + CLAW_TOP_CP_DX, head_bottom_y + CLAW_TOP_CP_DY, claw_start_x + CLAW_TIP_DX, CLAW_TIP_DY).Q(claw_start_x + CLAW_BOT_CP_DX, head_top_y + CLAW_BOT_CP_DY, claw_start_x, head_top_y).Z()
t_note_group.append(claw_part)

# Shape 1: Back Protrusion (Skewed Path)
back_shape = Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
p_A = (head_rect_left_x, head_top_y)
p_B = (head_rect_left_x, head_bottom_y)
p_C = (head_rect_left_x - BACK_SHAPE_WIDTH, head_bottom_y)
p_D = (head_rect_left_x - BACK_SHAPE_WIDTH + HANDLE_SKEW_OFFSET, head_top_y)
back_shape.M(*p_A).L(*p_D).L(*p_C).L(*p_B).Z()
t_note_group.append(back_shape)

# Handle (Stem of T_NOTE)
handle_top_y = head_bottom_y + HANDLE_VERTICAL_OFFSET
handle_bottom_y = handle_top_y + HANDLE_LENGTH
handle_top_left_x = -HANDLE_WIDTH/2 + HANDLE_HORIZONTAL_OFFSET
handle_top_right_x = HANDLE_WIDTH/2 + HANDLE_HORIZONTAL_OFFSET
handle_bottom_left_x = handle_top_left_x + HANDLE_SKEW_OFFSET
handle_bottom_right_x = handle_top_right_x + HANDLE_SKEW_OFFSET

handle = Path(stroke=T_NOTE_STROKE_COLOR, stroke_width=T_NOTE_STROKE_WIDTH, fill=T_NOTE_FILL_COLOR)
handle.M(handle_top_left_x, handle_top_y).L(handle_top_right_x, handle_top_y).L(handle_bottom_right_x, handle_bottom_y).L(handle_bottom_left_x, handle_bottom_y).Z()
t_note_group.append(handle)

# Shape 2: Bottom Ellipse/Oval (Shifted independently)
base_ellipse_cx = (handle_bottom_left_x + handle_bottom_right_x) / 2
ellipse_cx = base_ellipse_cx + OVAL_HORIZONTAL_OFFSET
ellipse_cy = handle_bottom_y + BOTTOM_ELLIPSE_Y_OFFSET
ellipse_transform = None
if OVAL_ROTATION_DEGREE != 0:
    ellipse_transform = f"rotate({OVAL_ROTATION_DEGREE}, {ellipse_cx}, {ellipse_cy})"

bottom_ellipse = Ellipse(ellipse_cx, ellipse_cy, BOTTOM_ELLIPSE_RX, BOTTOM_ELLIPSE_RY,
                         stroke=T_NOTE_STROKE_COLOR,
                         stroke_width=T_NOTE_STROKE_WIDTH,
                         fill=T_NOTE_FILL_COLOR,
                         transform=ellipse_transform
                         )
t_note_group.append(bottom_ellipse)

# Add the T_NOTE group to the main group
main_group.append(t_note_group)

dwg.append(main_group)

# --- Save the SVG ---
suffix = "final" if APPLY_GLITCH_FILTER else "shape_only"
dwg.save_svg(f'transpose_real_logo_{suffix}.svg')
print(f"SVG logo 'transpose_real_logo_{suffix}.svg' saved.")