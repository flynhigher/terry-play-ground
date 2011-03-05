ipClass :: IPClassifier(tcp,
			-);
FromDump(d4.dump, STOP true, TIMING true) -> ipClass;
prioSch :: PrioSched;
ipClass[0] -> match :: StringMatch("ilovenyc");
match[0] -> Queue() -> BandwidthShaper(93750) -> [0] prioSch;
match[1] -> Discard;
ipClass[1] -> Queue() -> [1] prioSch;
prioSch -> BandwidthShaper(128000) -> SetTimestamp -> ToDump(o4.dump, ENCAP IP);
