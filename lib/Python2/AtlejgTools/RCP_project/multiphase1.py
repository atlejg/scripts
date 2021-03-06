# north komsomolskoja for ali.
rho_o = 920.                 # kg/m3
rho_g = 87.5                 # kg/m3
mu_o  = 115.                 # cp
mu_g  = 0.012                # cp
vp = [1000., 1., 1e-3, 2.4, 0.65]  # valve parameters

RHO_EXP = 2.
MU0     = 0.

if len(sys.argv) > 1:
   vp[2] = float(sys.argv[1])
   vp[3] = float(sys.argv[2])
   vp[4] = float(sys.argv[3])
   RHO_EXP = float(sys.argv[4])
   USE_STD_AICD_FUNC = int(sys.argv[5])
   MU0               = float(sys.argv[6])
else:
   vp = [1000., 1., 2e-4, 3., 0.65]  # valve parameters
   USE_STD_AICD_FUNC = 1

COLOUR = 'gbkmcr'

def _oil():
   q  = r_[158, 339, 388, 456, 545, 704]
   dp = r_[ 0.9, 3, 5, 10, 20, 40]
   return (q, dp)

def _gas():
   q  = r_[ 91,	128, 199,203, 217, 243, 269, 293, 327, 354, 374, 371, 353]
   dp = r_[ 0.5, 1, 1.8, 3, 4, 6, 8, 10, 12, 15, 20, 30, 40]
   return (q, dp)

def rcp_coeff(rho, mu, rho_cal, mu_cal, cnst, y):
   '''
   for debug purposes, its useful to have this isolated
   [rho] = kg/m3
   [mu]  = cp
   [q]   = l/h
   '''
   if USE_STD_AICD_FUNC: return (rho**2/rho_cal) * (mu_cal/mu)**y * cnst
   else                : return (rho**RHO_EXP/rho_cal) * (mu_cal/(mu+MU0))**y * cnst

def rcp_dp3(rcp_params, rho, mu, q):
   '''
   [rho] = kg/m3
   [mu]  = cp
   [q]   = l/h
   [dp]  = bar
   rcp_params: (rho_cal, mu_cal, cnst, x, y)
   '''
   q = q * 24. / 1000. # convert to m3/day
   rho_cal, mu_cal, cnst, x, y = rcp_params
   return rcp_coeff(rho, mu, rho_cal, mu_cal, cnst, y) * q**x

# plot valve characteristics for varying gvf's
gvf = linspace(0.,1, 15)
gvf = r_[0, 0.25, 0.5, 0.75, 0.9, 1]
q = linspace(1, 2000, 100)
rm = VC.rho_mix(rho_o,rho_g, gvf)
vm = VC.mu_mix(mu_o,mu_g, gvf)
fig = figure()
print fig.number
dr = 1./len(gvf)
for i in range(len(gvf)):
   #if gvf[i] in (0,1): ls = '-'
   #else              : ls = '--'
   #col = (dr*i,0,1-dr*i)
   #plot(q, VC.rcp_dp3(vp, rm[i], vm[i], q), color=col, linestyle=ls)
   ls = '--'
   plot(q, rcp_dp3(vp, rm[i], vm[i], q), color=COLOUR[i], linestyle=ls)
#ylim(0,50)
# include multiphase testdata
dp_exp = r_[3,10,20,30]
plot((360,670,950,1160), dp_exp, 'bo', label='25%')
plot((400,780,1080,1310), dp_exp, 'ko', label='50%')
plot((510,890,1290,1550), dp_exp, 'mo', label='75%')
plot((510,890,1290,1660), dp_exp, 'co', label='90%')
legend(loc='best')
# include singlephase (testdata)
plot(_oil()[0], _oil()[1], 'gs', markersize=5)
plot(_gas()[0], _gas()[1], 'rv', markersize=5)
#title('blue=oil, red= gas')
title('%.2e %.2f %.2f [%.2f %.2f]' % (vp[2],vp[3],vp[4], RHO_EXP, MU0))
qt = xticks()[0]
xticks(qt, ['%i' % (x*24/1000.) for x in qt])
xlabel('flow rate [m3/d]')
ylabel('dp valve [bar]')
axis((0,1800, 0,42))
grid(True)

# plot flowrate at given dp for varying gvf's
if False:
   gvf = linspace(0,1, 500)
   dp0 = 40   # bar
   rm = VC.rho_mix(rho_o,rho_g, gvf)
   vm = VC.mu_mix(mu_o,mu_g, gvf)
   figure()
   q0 = zeros(len(gvf))
   for i in range(len(gvf)):
      q0[i] = VC.rcp_flowr3(vp, rm[i], vm[i], dp0)
   plot(gvf, q0, '.-')
   xlabel('gvf [-]')
   ylabel('flow rate [l/h] @ %i bar dp'%dp0)
   xlim(0, 1.05)
   grid(True)

show()
