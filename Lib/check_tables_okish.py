import cmor,numpy
from cmor.check_CMOR_compliant import readTable

tables = """CMIP5_3hr     CMIP5_6hrPlev CMIP5_LImon   CMIP5_OImon   CMIP5_Omon    CMIP5_aero    CMIP5_cfDay   CMIP5_cfOff   CMIP5_day     CMIP5_grids CMIP5_6hrLev  CMIP5_Amon    CMIP5_Lmon    CMIP5_Oclim   CMIP5_Oyr     CMIP5_cf3hr   CMIP5_cfMon   CMIP5_cfSites CMIP5_fx"""
tables = """CMIP5_3hr     CMIP5_6hrPlev CMIP5_LImon   CMIP5_OImon   CMIP5_Omon    CMIP5_aero    CMIP5_cfDay   CMIP5_cfOff   CMIP5_day      CMIP5_6hrLev  CMIP5_Amon    CMIP5_Lmon    CMIP5_Oclim   CMIP5_Oyr     CMIP5_cf3hr   CMIP5_cfMon    CMIP5_fx"""

for t in tables.split():
    print 'Table:',t
    tnm = "Tables/%s" % t
    tbl = readTable(tnm)
    vr = tbl['variable']
    ax = tbl['axis']
    g = tbl['general']
    cmor.setup(inpath='Tables',set_verbosity=cmor.CMOR_QUIET,
               netcdf_file_action = cmor.CMOR_REPLACE,exit_control=cmor.CMOR_EXIT_ON_MAJOR)
    cmor.dataset('pre-industrial control', 'ukmo', 'HadCM3', '360_day',
                 institute_id = 'ukmo',
                 model_id = 'HadCM3',
                 forcing="TO",
                 contact="Derek Jeter",
                 history = 'some global history',
                 parent_experiment_id="lgm",branch_time=0)
    cmor.load_table(tnm)
    dims={}
    print '\tDimensions:'
    for a in ax:
        A=ax[a]
        print '\t\t',a,A.get('type','notype')
        mn = float(A.get("valid_min",-1.e20))
        mx = float(A.get("valid_max",1.e20))
        val = (mn+mx)/2.
        val = numpy.array([float(A.get("value",val)),])
        if A.has_key("requested"):
            val=[]
            isnum=True
            for v in A['requested']:
                try:
                    val.append(float(v))
                except:
                    isnum=False
                    val.append(v)
            if isnum: val=numpy.array(val)
        kargs = {'table_entry':a,'units':A.get('units','1'),'coord_vals':val}
        if A.get("must_have_bounds","no")=="yes":
            if A.get("requested_bounds",None) is not None:
                rb = A['requested_bounds']
                print rb, 'vs', A.get('requested',None)
                bnds=[]
                rsp=rb.split()
                if len(rsp)>2 and rsp[1]!=rsp[2]:
                    for b in rsp:
                        print b
                        bnds.append(float(b))                        
                else:
                    for b in rsp[::2]:
                        print b
                        bnds.append(float(b))
                    bnds.append(float(rsp[-1]))
                kargs['cell_bounds']=numpy.array(bnds)
                if A.get('requested',None) is None:
                    vals=[]
                    for i in range(len(bnds)-1):
                        vals.append((bnds[i]+bnds[i+1])/2.)
                    vals=numpy.array(vals)
                    kargs['coord_vals']=vals
            elif A.get("bounds_values",None) is None:
                if A.get("axis","N")=='T':
                    kargs['cell_bounds']=numpy.array([val[0],val[0]+float(g['approx_interval'])])
                else:
                    if A.get("stored_direction","increasing")=="increasing":
                        kargs['cell_bounds']=numpy.array([val[0]-.1*abs(val[0]),val[0]+.1*abs(val[0])])
                    else:
                        kargs['cell_bounds']=numpy.array([val[0]+.1*abs(val[0]),val[0]-.1*abs(val[0])])
            else:
                b=A["bounds_values"].split()
                kargs['cell_bounds']=numpy.array([float(b[0]),float(b[1])])
        dims[a]=cmor.axis(**kargs)
    print '\tVariables:'
    for v in vr.keys():
        Vr=vr[v]
        print '\t\t',v,':',
        try:
            print Vr['dimensions']
        except:
            print 'No dims, skipped'
            continue
        vdims=[]
        for d in Vr['dimensions']:
            if d=='olevel':
                vdims.append(dims['depth_coord'])
            elif d=='alevel':
                vdims.append(dims['smooth_level'])
            else:
                vdims.append(dims[d])
        kargs={}
        if Vr.has_key("positive"):
            kargs['positive']=Vr['positive']
        V=cmor.variable(table_entry=v,units=Vr.get('units','1'),axis_ids=numpy.array(vdims),**kargs)
    cmor.close()
print 'Done'
