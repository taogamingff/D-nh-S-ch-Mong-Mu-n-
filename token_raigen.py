import requests as _rq
#code by @raigenffofc 
#code by @raigenffofc 
#modified by raigen rohan
xxx_t = None

def _chk(_dx, _rg):
    if _rg == "IND":
        if _dx.get('status') in ['success', 'live']:
            return _dx.get('token')
    elif _rg in ["BR", "US", "SAC", "NA"]:
        if isinstance(_dx, dict) and 'token' in _dx:
            return _dx['token']
    else: 
        if _dx.get('status') == 'live':
            return _dx.get('token')
    return None

def get_xxx_sync(_rg):
    global xxx_t
    
    _x = {
        "IND": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>4939177321'qbttxpse>D52C11:9:67BF8C8:G863GDB984D858171D82E4D28GCF58:5G6FC:CE82E5EB:6",
        "BR": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>4898592424'qbttxpse>KmPjwQfptbvW1m:TH7hxL4:mI4y3lKlP",
        "US": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>4898592424'qbttxpse>KmPjwQfptbvW1m:TH7hxL4:mI4y3lKlP",
        "SAC": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>4898592424'qbttxpse>KmPjwQfptbvW1m:TH7hxL4:mI4y3lKlP",
        "NA": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>4898592424'qbttxpse>KmPjwQfptbvW1m:TH7hxL4:mI4y3lKlP",
        "default": "iuuqt;00kxu.sbjhfo.pc63/wfsdfm/bqq0uplfo@vje>5262728933'qbttxpse>:EE4369GBB1F6E1CF21DDD62G58:98G6:85DC1GCG8773F3DG6C:24:B5E825B3D"
    }    
    
    _z = _x.get(_rg, _x["default"])
    _p = "".join(chr(ord(_c) - 1) for _c in _z)
    
    try:
        _res = _rq.get(_p, timeout=10)
        if _res.status_code == 200:
            _d = _res.json()
            _tk = _chk(_d, _rg)
            if _tk:
                xxx_t = _tk
                print(f"[+] Sys -> {_rg}")
                return xxx_t
            else:
                print(f"[-] Null")
        else:
            print(f"[-] Code {_res.status_code}")
    except Exception as _e:
        print(f"[-] Err: {_e}")   
    return None

def ensure_xxx_sync(_rg):
    global xxx_t
    if not xxx_t:
        return get_xxx_sync(_rg)
    return xxx_t
#code by @raigenffofc 
#code by @raigenffofc 
#modified by raigen rohan