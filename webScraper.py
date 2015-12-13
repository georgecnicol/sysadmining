# George Nicol
# python 3.4
# 11/2015
# WebScraper - Version 1.0
# Copyright (c) 2015 Embedded Acumen, LLC
# All rights reserved.
#
#    Unless you have express writen permission from the Copyright Holder, any
# use of or distribution of this software or portions of it, including, but not
# limited to, reimplementations, modifications and derived work of it, in
# either source code or any other form, as well as any other software using or
# referencing it in any way, may NOT be sold for commercial gain, must be
# covered by this very same license, and must retain this copyright notice and
# this license.
#    Neither the name of the Copyright Holder nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THERE IS NO WARRANTY FOR THE SOFTWARE, TO THE EXTENT PERMITTED BY APPLICABLE
# LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR
# OTHER PARTIES PROVIDE THE SOFTWARE "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
# ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SOFTWARE IS WITH YOU.
# SHOULD THE SOFTWARE PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY
# SERVICING, REPAIR OR CORRECTION.
#
# IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL
# ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
# THE SOFTWARE AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
# GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE
# OR INABILITY TO USE THE SOFTWARE (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR
# DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR
# A FAILURE OF THE SOFTWARE TO OPERATE WITH ANY OTHER SOFTWARE), EVEN IF SUCH
# HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
#
# BY USING THIS SOFTWARE USER AGREES THAT USER WILL NOT DO SO FOR ANY PURPOSES
# OTHER THAN LAWFUL RESEARCH.

# TODO
# need to follow re-directs...



import re, sys, urllib.request
import argparse


# --- improve this list over time
regularEmail='[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\-]+?\.[a-zA-Z]+'
typicalForum='[a-zA-Z0-9_\.]+\ at\ [a-zA-Z0-9_\-]+?\ dot\ [a-zA-Z]+'
hybridEmail='[a-zA-Z0-9_\.]+\ at\ [a-zA-Z0-9_\-]+?.[a-zA-Z]+'
moreLinks=True
activeLinks=[]
visitedLinks=[]
emailsHarvested=[]
phonesHarvested=[]
userNames=[]

class Ooops(Exception):
  def __init__(self, value):
    self.value=value
  def __str__(self):
    return repr(self.value)

def usage():
    print("usage: {0} http://www.example.org".format(sys.argv[0]))
    sys.exit(1)


def scrape(address, baseURL):
  print("Processing {0}".format(address))
  wholeLink=[]
  html=urllib.request.urlopen(address, None, 3).read().decode('utf-8')
  links = re.findall("a href=\"(\S+)\"", html)
  for link in links:
    try:
      # not html files - try block will handle
      # if link.endswith("pdf"):
      # pass
      if re.findall(baseURL, link):
        wholeLink.append(link)
      elif link.startswith("//"):
        pass
      elif link.startswith("/"):
        wholeLink.append(baseURL+link)
    except:
      pass
#    elif link.startswith("../"):
#    # this should work but needs testing
#    address=args.URL[0].split("/")
#    address=address[:-1]
#    for item in shorterSplit:
#      newAddress+=item+"/"
#    wholeLink.append(newaddress+link.lstrip(".."))
  email = re.findall(regularEmail, html)
  #email += re.findall(typicalForum, html)
  #email += re.findall(hybridEmail, html)
  phone = re.findall('[0-9]{3}[^0-9a-zA-Z][0-9]{3}[^0-9a-zA-Z][0-9]{4}', html)

  return(wholeLink,email,phone)

# process the incoming URL
# grab the domain for later to ensure that the scraper doesn't go beyond the domain.
# parse dem args
# URL=sys.argv[1]

def run():
  parser = argparse.ArgumentParser(
        description="Scrape a domain for emails, user names and phone numbers ...",
        epilog="... because sometimes we need to know that stuff")

  parser.add_argument('-u', dest='URL', action='store', nargs=1, required=True, help="ip or URL")
  args, unknown = parser.parse_known_args()


  # format the domain or ip into what we need.
  try:
    args.URL[0]=args.URL[0].strip() # not realy needed but maybe someone cut and paste and put in quotes
                                    # other than that: garbage in, garbage out.
    if not args.URL[0].startswith("http://") and not args.URL[0].startswith("https://"):
      args.URL[0]="http://"+args.URL[0]
  # in retrospect I don't think there is a reason to have this?
  #  if not args.URL[0].endswith("/"):
  #    args.URL[0]+='/'


  except Ooops as e:
    print("{0}".format(e.value))
    usage()

  # this is the domain/ip/directory that will be scraped. This is used to ensure the
  # tool only goes down - not out or across to an external site - from here.
  if args.URL[0].startswith("https://"):
    coreElement=args.URL[0][8:]
  else:
    coreElement=args.URL[0][7:]
  activeLinks.append(args.URL[0])

  while len(activeLinks) != 0:
    try:
      current=activeLinks[0]
      if len(re.findall(coreElement, current)) == 0:
        activeLinks.remove(current)
      elif current in visitedLinks:
        activeLinks.remove(current)
      else:
        visitedLinks.append(current)
        activeLinks.remove(current)
        temp=scrape(current, args.URL[0])
        for item in temp[0]:
          if item not in visitedLinks:
            activeLinks.append(item)
        for item in temp[1]:
          if item not in emailsHarvested:
            emailsHarvested.append(item)
        for item in temp[2]:  # this needs more wotk, we don't necessarily want a bunch of valid phone numbers with no
                              # related contact information
          if item not in phonesHarvested:
            phonesHarvested.append(item)
    except KeyboardInterrupt as e:
      print("")
      sys.exit(0)

    except:
      pass

  if len(phonesHarvested) > 0:
    print("\n\nphone numbers found")
    for u in phonesHarvested:
      print(u)
  if len(emailsHarvested) > 0:
    print("\n\nemails: ")
    for u in emailsHarvested:
      print(u)
    print("\n\npossible user account names:")
    for u in emailsHarvested:
      u=u.split("@")[0]
      print(u)


if __name__ == '__main__':
  run()

