import math
import matplotlib.pyplot as plt
import string

def insert_scine(tmpl, fig, L, d, k_pene, k_deform):

    # The values of 'time'.
    steps = 1000
    T = [(L / (k_pene + k_deform)) * (i / float(steps)) for i in range(steps)]

    # The length of the electrode inside of, enveloped by, and outside
    # of the cell over time.
    L_intra = [k_pene * t for t in T]
    L_env = [k_deform * t for t in T]
    L_extra = [L - l[0] - l[1] for l in zip(L_intra, L_env)]

    p = fig.add_subplot(2, 2, 1)
    p.set_title('Electrode length')
    p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    p.set_ylabel('m')
    p.plot(T, L_extra, 'r', T, L_intra, 'g', T, L_env, 'b')
    p.legend(['L_extra', 'L_intra', 'L_env'])

    # The surface area of the electrode inside of, enveloped by, and
    # outside of the cell over time.
    cap = math.pi * pow(d / 2, 2)
    A_per_L = math.pi * d
    A_intra = [cap + (A_per_L * l) for l in L_intra]
    A_env = [A_per_L * l for l in L_env]
    A_extra = [A_per_L * l for l in L_extra]

    # The surface area of the membrane enveloping the electrode over
    # time, where the enveloping membrane is a cylinder with diameter
    # = electrode diameter + 100nm, and with length = electrode
    # length.
    A_membrane = [math.pi * (d + 100e-9) * l for l in L_env]

    p = fig.add_subplot(2, 2, 2)
    p.set_title('Electrode surface area')
    p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    p.set_ylabel('m^2')
    p.plot(T, A_extra, 'r', T, A_intra, 'g', T, A_env, 'b', T, A_membrane, 'y')
    p.legend(['A_extra', 'A_intra', 'A_env', 'A_membrane'])

    # The seal resistance over time.
    R_seal = [10e9 * l / (d * math.pi) for l in L_env]

    #eei_circuit(q0=50000, n=0.5)

tmpl = string.Template(open('eei.cir', 'r').read())
def eei_circuit(**kwargs):
    fn = ''
    for k, v in kwargs.items():
        fn = '%s%s_%s' % (fn + '__' if fn else '', k, str(v))
    open('eei/%s.cir' % fn, 'w').write(tmpl.substitute(kwargs))

fig = plt.figure()
insert_scine(tmpl, fig, 5000e-9, 500e-9, 2, 1)
fig.show()
raw_input('enter to continue')

# compartmental(num, cond, k, alpha, tmax,A_membrane, A_env,  A_intra, A_extra, Rseal)


# //generates values for each comparemental variable 
# function compartmental(num, cond, k, alpha, tmax,A_mem, A_env, A_intra, A_extra, Rseal)

# //calculate resistance between each compartment
# 	make /o/n=(tmax) Rseal_c = Rseal / num

	
# //calculate compartmental membrane resistance	
# 	//calculate trans membrane conductance over time
# 	make /o/n=(tmax) Stm = cond * A_mem
# 	//divide by number of compartments
# 	stm /= num
# 	//calculate resistance
# 	make /o/n=(tmax) Rtm_c = stm^-1
# 	killwaves stm //kill temp wave

# //calculate compartmental capacitance

# 	make /o/n=(tmax) Ctm_c= (A_mem * 0.01)/ num

# //create compartmental cpe

# 	//stores 1 cpe for each time point in a tmax by 8000 matrix
# 	//remember that the frequency wave (fwave) contains the corresponding x values to be plotted against the cpe y values for each column in the matrix
	
# 	variable kscaled // k* area of electrode segment 
# 	variable count
	
# 	make /c/o/n=(8000,tmax) cpe_env
# 	cpe_env[][0]=1e100
# 	t=1
# 	do
# 		kscaled = k * (A_env[t]/num)
# 		cpe(alpha, kscaled, .001, 100000)
# 		wave cpe_z //initialize newly created wave
# 			count =0
# 			do
# 			cpe_env[count][t]= cpe_z[count]
# 			count +=1
# 			while (count < 8000)
# 		t+=1	
# 	while (t <tmax)

		
# //create intracellular cpe

# 	make /c/o/n=(8000,tmax) cpe_intra 
# 	cpe_intra[][0]=1e100
# 	t=1
# 	do
# 		kscaled = k * (A_intra[t])
# 		cpe(alpha, kscaled, .001, 100000)
# 		wave cpe_z //initialize newly created wave
# 			count =0
# 			do
# 			cpe_intra[count][t]= cpe_z[count]
# 			count +=1
# 			while (count < 8000)
# 		t+=1	
# 	while (t <tmax)

# //create extracellular cpe

# make /c/o/n=(8000,tmax) cpe_extra
# 	cpe_extra[][7999]=1e100
# 	t=0
# 	do
# 		kscaled = k * (A_extra[t])
# 		cpe(alpha, kscaled, .001, 100000)
# 		wave cpe_z //initialize newly created wave
# 			count =0
# 			do
# 			cpe_extra[count][t]= cpe_z[count]
# 			count +=1
# 			while (count < 7999)
# 		t+=1	
# 	while (t <tmax)



# end

















# /////////////////////////////////////////////////////////playing with CPE



# 			function sweepk(kstart,kstop,a)
# 				//calls function cpe
# 				//sweep k constant on log scale for a given alpha

# 			variable kstart
# 			variable kstop
# 			variable a 

# 			variable k
# 			variable increment= (log(kstop)-log(kstart))/10           //
# 			variable f1= 0.001
# 			variable f2= 1e5
# 			variable i=log(kstart)         //initialize at 1

		
# 					//open graph
# 					make /c/o/n=1 blank= nan
# 					display /k=1 blank
# 					ModifyGraph log=1

# 			do
# 				cpe(a,10^i,f1,f2)
# 				i+= increment
# 				while (i < log(kstop))		//stop at alpha=1 (capacitor)


# 					//remove blank
# 					RemoveFromGraph blank


# 			end

# 			function sweepa(k)
# 				//calls function cpe
# 				//for a given constant, generate a ton of CPEs with varying alphas

# 			variable k 
# 			variable f1= 0.001
# 			variable f2= 1e5
# 			variable i=0         //initialize at aplha=0 (resistor)

		
# 					//open graph
# 					make /c/o/n=1 blank= nan
# 					display /k=1 blank
# 					ModifyGraph log=1

# 			do
# 				cpe(i,k,f1,f2)
# 				i+=.02
# 				while (i <1.02)		//stop at alpha=1 (capacitor)


# 					//remove blank
# 					RemoveFromGraph blank


# 			end


# ///////////////////////////////////////////////////////////////





# function CPE(alpha,k,fstart,fstop)
# 	//produces a constant phase element with freq dependence 1/ (f^alpha) and constant k
# 	//here k incluces the specific capacitance at 1 Hz (Cspec) times the electrode area
	
# variable alpha
# variable k
# variable fstart
# variable fstop
# variable f
# variable z
# variable points 
# variable /c im = (-1)^.5

# points = (log(fstop)-log(fstart))*1000

# //make xwave for log(frequency) with 1k points per decade
# 	make /o/n=2 xwave
# 	xwave[0] =log(fstart)
# 	xwave[1] =log(fstop)
# 	Interpolate2/T=1/N=(points)/Y=xwave_L xwave
# 	duplicate /o xwave_L, xwave
# 	killwaves xwave_L


# //make a frequency wave to plot against the cpe
# 	make /o/n=(points) fwave
# 	variable i=0
# 	variable x
# 	do
# 		x = xwave[i]
# 		fwave[i] = 10^x
# 		i += 1
# 	while (i < points)

# // make a constant phase element with impedance at frequencies "fwave"

# 	make  /o/c/n=(points) cpe_Z
# 	i=0
# 	do
# 		x=fwave[i]
# 		cpe_z[i]= 1 / (k*(x*im)^alpha)
# 		i +=1
# 	while (i < points)

# //rename output wave, kill temp files, and display all CPEs

# 	//this old naming system was more informative before I made the cpe function a sub-function to insert_scine
# 		//string output = "CPE_k=" + num2str(k) + "a=" +num2str(alpha)
# 		//duplicate /o cpe_z $(output)
# 		//killwaves cpe_z, xwave

# 	//	killwaves xwave

# 	//now defunct graphing
# 		//AppendToGraph $(output) vs fwave
# 	//	SetAxis bottom (fstart), (fstop)
# 	//	ModifyGraph cmplxMode=3

# end
