/*
 * stringmatch.{cc,hh} -- try match a certain keyword in packets' contents
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
#include <click/confparse.hh>
#include <click/error.hh>
#include <click/router.hh>
#include "stringmatch.hh"
CLICK_DECLS

StringMatch::StringMatch()
{
}

StringMatch::~StringMatch()
{
}

int
StringMatch::configure(Vector<String> &conf, ErrorHandler *errh)
{
  _word = "";
  if (cp_va_parse(conf, this, errh,
	cpString, "keyword", &_word,
	cpEnd) < 0)
    return -1;
  //click_chatter("%{element}: push kw %s ", this, _word.c_str());
  return 0;
}

void
StringMatch::push(int port, Packet *p)
{
  int s = 0;
  if (noutputs() < 2) {
    click_chatter("%s{element}: requires at least two output ports", this);
    exit(1);
  }
//  click_chatter("%{element}: push kw %s pkt data len %d",
//                       this, _word.c_str(), p->end_data() - p->data());
  String dataStr = String();
  const unsigned char *data = p->data();
  for (; data < p->end_data(); data++) {
    dataStr += ((*data < 32 || *data > 126) ? '.' : *data);
  }
//  click_chatter("%{element}: packet string %s", this, dataStr.c_str());
  int index = dataStr.find_left(_word);
//  click_chatter("%{element}: push index %d", this, index);
  (index > -1) ? output(1).push(p) : output(0).push(p);
}

CLICK_ENDDECLS
EXPORT_ELEMENT(StringMatch)
ELEMENT_MT_SAFE(StringMatch)
