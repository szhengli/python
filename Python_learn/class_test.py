glb = "gloal"

def maker(n):
    loc="local"
    def action(x):
        inside = "inside"
        print("%s from global " +
              "%s from n  " +
              "%s from local " +
              "%s from x " +
              "%s from inside" % (glb, n, loc,x, inside ))
    return action

m=maker("james-n")

