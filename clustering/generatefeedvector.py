import feedparser
import re
import sys


# Returns title and dictionary of word counts for an RSS feed
def get_word_counts(url):
   # Parse the feed
   d = feedparser.parse(url)
   wc = {}
   
   # Loop over all the entries
   for e in d.entries:
      if 'summary' in e: summary = e.summary
      else: summary = e.description
      
      # Extract a list of words
      words = get_words(e.title + ' ' + summary)
      for word in words:
         wc.setdefault(word, 0)
         wc[word] += 1
   if 'title' in d.feed: title = d.feed.title
   else: title = 'no title'
   return title, wc

def get_words(html):
   # Remove all the HTML tags
   txt = re.compile(r'<[^>]+>').sub('', html)
   
   # Split words by all non-alpha characters
   words = re.compile(r'[^A-Z^a-z]+').split(txt)
   
   return [word.lower() for word in words if word != '']

# Keeps track of number of blogs each word appears in
apcount = {}

# Keeps track of word count dictionary for each title
wordcounts = {}
feedlist = file(sys.argv[1]).readlines()

for feedurl in feedlist:
   title, wc = get_word_counts(feedurl)
   wordcounts[title] = wc
   for word, count in wc.items():
      apcount.setdefault(word, 0)
      if count > 1:
         apcount[word] += 1

# Keep track of words that appear in more than 10%
# but less than 50% of the blogs
wordlist = []
for word, blog_count in apcount.items():
   frac = float(blog_count)/len(feedlist)
   if frac > 0.1 and frac < 0.5: wordlist.append(word)

out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
   out.write(blog)
   for word in wordlist:
      if word in wc: out.write('\t%d' % wc[word])
      else: out.write('\t0')
   out.write('\n')