ipClass :: IPClassifier(tcp,
			-);
FromDump(d2.dump, STOP true, TIMING true) -> ipClass;
prioSch :: PrioSched;
ipClass[0] -> Queue() -> BandwidthShaper(93750) -> [0] prioSch;
ipClass[1] -> Queue() -> [1] prioSch;
prioSch -> BandwidthShaper(128000) -> SetTimestamp -> ToDump(o2.dump, ENCAP IP);
