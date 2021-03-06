'''
-------------------
atle j. gyllensten
agy@statoil.com
Q4 - 2017
-------------------
given a well trajectory, with arbitrary segments, it will resample this into
sections of equal length (typically 12m).
this is done by walking along segments and finding intersects that are 12m away from current
point. need to solve 2nd-order equation for this, but only using the largest root.
#
this functionality is needed for Reveal when modelling inflow control, since it does not scale properly.
Reveal documentation says:
   All fixed length devices (Equalizer, ICV and ICDs) have flow areas and consequent pressure drops
   that are for a specific device length.  Therefore the same pressure drop to rate relation
   will apply regardless of the actual length of device that is set.  The devices should
   therefore usually be placed with their correct lengths in the equipment location screen;
   warnings are given if this is not the case.  This is in contrast to the screens and
   orifice, where the effective flow is input per unit length.
'''
JOINT_L = 12. # joint length

def read_trajectory(fnm, filter_l, skiprows=1):
    '''
    read trajectory from text file.
    # input
     fnm      : name of trajectory file
     filter_l : segments smaller than this will be removed
     skiprows : number of header lines in input file that will be discarded
    # output
     matrix representing trajectory
    # file format:
    #
    <header lines>
    ...
    x1  y1  z1
    x2  y2  z2
    x3  y3  z3
    .   .   .
    .   .   .
    .   .   .
    xN  yN  zN
    '''
    raw    = loadtxt(fnm, skiprows=skiprows)   # segment coordinates
    if filter_l <= 0: return raw
    # filter trajectory
    i    = 0
    x0   = raw[0]
    traj = [x0]
    while True:
        i += 1
        if i == len(raw)              : break
        if norm(x0-raw[i]) < filter_l : continue
        # most often...
        x0 = raw[i]
        traj.append(x0)
    return (array(traj))

def write_joints(joints, fnm, verbose=0):
    if verbose: print('number of segments = ', (len(joints)-1))
    f = open(fnm, 'w')
    for j in range(len(joints)):
        if verbose and j < len(joints)-1:
            print(joints[j+1]-joints[j], '==>', norm(joints[j+1]-joints[j]))
        f.write('%.8e;  %.8e;  %.8e\n'%tuple(joints[j]))
    f.close()
    print(fnm, 'was created')

def create_regular_trajectory(fnm, segm_l=JOINT_L, filter_l=JOINT_L/10.):
    traj = read_trajectory(fnm, filter_l)
    # init
    x0     = traj[0]
    x1     = traj[1]
    joints = [x0]
    i      = 1
    dx     = zeros(3)
    r      = x1 - x0
    # loop
    while True:
        if i == len(traj)-1: break
        l = norm(r)                                              # for convinience
        a = l**2; b = 2*dot(dx,r); c = dot(dx,dx) - segm_l**2    # a-b-c formula for 2nd-order polynomial
        expr = b**2 - 4*a*c                                      # sqrt-argument
        if expr > 0:
            s = (-b + sqrt(expr)) / (2*a)
            x1 = x0 + dx + s*r
            x = x1 - x0 - dx                                      # component along r-vector
        if (expr < 0) or (norm(x) > l):
            # it did not intersect. go to next segment
            dx = traj[i] - x0
            r  = traj[i+1] - traj[i]
            i += 1
        else:
            # it did interesect. keep it - and move on
            joints.append(x1)
            x0 = x1
            dx = zeros(3)
            r  = traj[i] - x0
    # write results
    write_joints(joints, UT.basename(fnm)+'_v2.csv')

if __name__ == '__main__':
    fnm = sys.argv[1]   # survey.txt
    create_regular_trajectory(fnm)
