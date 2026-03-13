import matplotlib.pyplot as plt
from splines import Bezier, BSpline, NURBS, CompositeCurve

b = Bezier([(50,300),(150,50),(250,550),(350,300)])
bs_ctrl = [(x, y+200) for (x,y) in [(400,100),(450,300),(500,200),(550,500),(600,250),(650,400)]]
bs = BSpline(bs_ctrl, degree=2)
weights = [1,2,1,0.5,1.5,1]
nurbs_ctrl = [(x, y+400) for x,y in bs_ctrl]
nurbs = NURBS(nurbs_ctrl, weights, degree=2)

comp = CompositeCurve([b, bs, nurbs], param_lengths=[1,1,1])

def sample_curve(curve, n=200):
    return curve.sample(n)

plt.figure(figsize=(10,6))
def draw_ctrl(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    plt.plot(xs, ys, marker='o', linestyle='--')

draw_ctrl(b.control)
draw_ctrl(bs.control)
draw_ctrl(nurbs.control)

bx, by = zip(*sample_curve(b,200))
plt.plot(bx, by)

bsx, bsy = zip(*sample_curve(bs,400))
plt.plot(bsx, bsy)

nx, ny = zip(*sample_curve(nurbs,400))
plt.plot(nx, ny)

cx, cy = zip(*sample_curve(comp,800))
plt.plot(cx, cy, linewidth=1)

plt.title("Bezier, B-Spline, NURBS (control polygons dashed)")
plt.axis('equal')
plt.axis('off')
out = "splines_test_output.png"
plt.savefig(out, bbox_inches='tight', dpi=150)
print("Saved:", out)