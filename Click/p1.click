ipClass :: IPClassifier(dst net 18.0.0.0/8,
			dst net 131.207.0.0/16,
			dst net 149.207.0.0/16,
			-);
FromDump(d1.dump, STOP true) -> CheckIPHeader -> ipClass;
ipClass[0] -> ToDump(o1-1.dump, ENCAP IP);
ipClass[1] -> ToDump(o1-2.dump, ENCAP IP);
ipClass[2] -> ToDump(o1-3.dump, ENCAP IP);
ipClass[3] -> Discard;
