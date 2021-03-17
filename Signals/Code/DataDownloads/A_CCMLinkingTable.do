* 1. CCM Linking table ---------------------------------------------------------
#delimit ;
local sql_statement
    SELECT a.gvkey, a.conm, a.tic, a.cusip, a.cik, a.sic, a.naics, b.linkprim, 
	       b.linktype, b.liid, b.lpermno, b.lpermco, b.linkdt, b.linkenddt
    FROM comp.names as a
	INNER JOIN crsp.ccmxpf_lnkhist as b
	ON a.gvkey = b.gvkey
	WHERE b.linktype in ('LC', 'LU')
	AND b.linkprim in ('P', 'C')
	ORDER BY a.gvkey;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear
export delimited "$pathDataIntermediate/CCMLinkingTable.csv", replace // For processing of IO-Momentum in R

rename linkdt timeLinkStart_d
rename linkenddt timeLinkEnd_d 
rename lpermno permno

compress
save "$pathDataIntermediate/CCMLinkingTable", replace

