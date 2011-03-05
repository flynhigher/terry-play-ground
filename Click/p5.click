ipClass :: IPClassifier(tcp,
			-);
FromDump(d5.dump, STOP true, TIMING true) -> ipClass;
prioSch :: PrioSched;
ipClass[0] -> match :: StringMatch("ilovenyc");
match[0] -> tcpQ :: Queue();
match[1] -> reset :: FakeTCPReset[0] -> tcpQ;
reset[1] -> tcpQ;
tcpQ -> BandwidthShaper(93750) -> [0] prioSch;
ipClass[1] -> Queue() -> [1] prioSch;
prioSch -> BandwidthShaper(128000) -> SetTimestamp -> ToDump(o5.dump, ENCAP IP);
