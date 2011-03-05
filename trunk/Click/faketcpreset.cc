/*
 * faketcpreset.{cc,hh} -- fake TCP reset packet 
 * Jinyang Li
 *
 * Copyright (c) 1999-2000 Massachusetts Institute of Technology
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, subject to the conditions
 * listed in the Click LICENSE file. These conditions include: you must
 * preserve this copyright notice, and you cannot mention the copyright
 * holders in advertising related to the Software without their permission.
 * The Software is provided WITHOUT ANY WARRANTY, EXPRESS OR IMPLIED. This
 * notice is a summary of the Click LICENSE file; the license in that file is
 * legally binding.
 */

#include <click/config.h>
#include "faketcpreset.hh"
#include <clicknet/ip.h>
#include <clicknet/tcp.h>
#include <click/confparse.hh>
#include <click/error.hh>
#include <click/glue.hh>
#ifdef CLICK_LINUXMODULE
# include <net/checksum.h>
#endif
CLICK_DECLS

FakeTCPReset::FakeTCPReset()
{
}

FakeTCPReset::~FakeTCPReset()
{
}

void
FakeTCPReset::push(int port, Packet *p)
{
  const click_ip *iph = p->ip_header();
  const click_tcp *tcph = p->tcp_header();

  if (!iph || iph->ip_p != IP_PROTO_TCP) {
    click_chatter("%{element}: not a tcp packet", this);
    p->kill();
    return;
  }

  //click_chatter("%{element}: faking tcp resets", this);
  //XXX generate a TCP reset packet for the TCP connection as represented by this packet and push it out of port 0, also push this pkt out of port 0
  output(0).push(make_tcp_reset(iph->ip_src, iph->ip_dst, tcph->th_sport, tcph->th_dport, tcph->th_seq, tcph->th_ack));
  output(0).push(p);

  //XXX also generate a TCP reset for the reverse direction of the TCp connection as represented by this packet and push it out of port 1.
  output(1).push(make_tcp_reset(iph->ip_dst, iph->ip_src, tcph->th_dport, tcph->th_sport, tcph->th_ack, tcph->th_seq));
}


Packet *
FakeTCPReset::make_tcp_reset(struct in_addr saddr, struct in_addr daddr,
                       uint16_t sport, uint16_t dport,
		       unsigned int seqn, unsigned int ackn)
{
  struct click_ip *ip;
  struct click_tcp *tcp;
  WritablePacket *q = Packet::make(sizeof(*ip) + sizeof(*tcp));
  if (q == 0) {
    click_chatter("in FakeTCPReset: cannot make packet!");
    assert(0);
  } 
  memset(q->data(), '\0', q->length());

  ip = (struct click_ip *) q->data();
  tcp = (struct click_tcp *) (ip + 1);
  q->set_ip_header(ip, sizeof(click_ip));
  
  // IP fields
  ip->ip_v = 4;
  ip->ip_hl = 5;
  ip->ip_tos = 0;
  ip->ip_len = htons(q->length());
  ip->ip_id = htons(0);
  ip->ip_off = htons(IP_DF);
  ip->ip_ttl = 255;
  ip->ip_p = IP_PROTO_TCP;
  ip->ip_sum = 0;
  ip->ip_src = saddr;
  ip->ip_dst = daddr;
  ip->ip_sum = click_in_cksum((unsigned char *)ip, sizeof(click_ip));

  // TCP fields
  tcp->th_sport = sport;
  tcp->th_dport = dport; 

  //XXX set TCP seqno and ack no.
  tcp->th_seq = seqn;
  tcp->th_ack = ackn;

  tcp->th_off = 5;
  
  //XXX set the TCP flags to indicate this is a RESET packet
  tcp->th_flags = TH_RST;

  tcp->th_win = htons(32120);
  tcp->th_sum = htons(0);
  tcp->th_urp = htons(0);

  // now calculate tcp header cksum
  unsigned csum = click_in_cksum((unsigned char *)tcp, sizeof(click_tcp));
  tcp->th_sum = click_in_cksum_pseudohdr(csum, ip, sizeof(click_tcp));

  return q;
}


CLICK_ENDDECLS
EXPORT_ELEMENT(FakeTCPReset)
