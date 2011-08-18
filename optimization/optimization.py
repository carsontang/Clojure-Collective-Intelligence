import time
import random
import math
   
people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
# Laguardia
destination='LGA'

schedule = [1,4,3,2,7,3,6,3,2,4,5,3]

def getminutes(t):
   x = time.strptime(t, '%H:%M')
   return x[3]*60 + x[4]

flights = {}

for line in file("schedule.txt"):
   origin,dest,depart,arrive,price = line.strip().split(",")
   flights.setdefault((origin, dest),[])
   
   # Add details to the list of possible flights
   flights[(origin, dest)].append((depart,arrive,int(price)))

def printschedule(r):
   print '%33s %18s' % ('Outgoing','Return')
   for d in range(len(r)/2):
      name = people[d][0]
      origin = people[d][1]
      out = flights[(origin,destination)][r[d]]
      ret = flights[(destination, origin)][r[d+1]]
      print '%10s%10s  %5s-%5s  $%3s  %5s-%5s  $%3s' % (name,origin,
                                                   out[0],out[1],out[2],
                                                   ret[0],ret[1],ret[2])

# modify function so that people who wait 2 hours or longer can rent car
def schedulecost(sol):
   totalprice = 0
   latestarrival = 0
   earliestdep = 24*60
   
   for d in range(len(sol)/2):
      # Get the inbound and outbound flights
      origin = people[d][1]
      outbound = flights[(origin, destination)][int(sol[d])]
      returnf = flights[(destination, origin)][int(sol[d+1])]
      
      # Total price is the price of all outbound and return flights
      totalprice += outbound[2]
      totalprice += returnf[2]
      
      # Track the latest arrival and earliest departure
      if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
      if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])
      
   # Every person must wait at the airport until the latest person arrives.
   # They also must arrive at the same time and wait for their flights.
   totalwait = 0
   for d in range(len(sol)/2):
      origin = people[d][1]
      outbound = flights[(origin, destination)][int(sol[d])]
      returnf = flights[(origin, destination)][int(sol[d+1])]
      totalwait += latestarrival-getminutes(outbound[1])
      totalwait += getminutes(returnf[0])-earliestdep
      
   # Does this solution require an extra day of car rental? That'll be $50.
   if latestarrival > earliestdep: totalprice += 50
   
   return totalprice+totalwait

def randomoptimize(domain, costf):
   best = 999999999
   bestr = None
   for i in range(1000):
      # Create a random solution
      r = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
      
      # Get the cost
      cost = costf(r)
      
      # Compare it to the best one so far
      if cost < best:
         best = cost
         bestr = r
         
   return r

def hillclimb(domain,costf):
   # Create a random solution
   sol=[random.randint(domain[i][0],domain[i][1])
      for i in range(len(domain))]
   
   # Main loop
   while 1:
      # Create list of neighboring solutions
      neighbors=[]

      for j in range(len(domain)):
         # One away in each direction
         if sol[j]>domain[j][0]:
            neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
         if sol[j]<domain[j][1]:
            neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
      
      # See what the best solution amongst the neighbors is
      current=costf(sol)
      best=current
      for j in range(len(neighbors)):
         cost=costf(neighbors[j])
         if cost<best:
            best=cost
            sol=neighbors[j]

      # If there's no improvement, then we've reached the top
      if best==current:
         break
   return sol

def rand_restart_hillclimb(domain,costf):
   sols = []
   # 10 random restarts
   for i in range(10):
      sol = hillclimb(domain, costf)
      sols.append(sol)
   
   # Best solution of hill climbs starting at different origins
   bestsol = sols[0]
   bestcost = costf(bestsol)
   
   for i in range(len(sols))[1:]:
      cost = costf(sols[i])
      if cost < bestcost:
         bestcost = cost
         bestsol = sols[i]
   
   return bestsol

def test():
   domain = [(0,8)]*(len(people)*2)
   
   print "Hill climb costs: "
   hill_cost = []
   for i in range(10):
      s = hillclimb(domain, schedulecost)
      cost = schedulecost(s)
      hill_cost.append(cost)
      print cost
   print "Average cost: " + str( sum(hill_cost) / len(hill_cost) )
   
   print "Randomize costs: "
   rand_cost = []
   for i in range(10):
      s = randomoptimize(domain, schedulecost)
      cost = schedulecost(s)
      rand_cost.append(cost)
      print cost
   print "Average cost: " + str( sum(rand_cost) / len(rand_cost) )
   
   '''
   print "Random restart hill climb costs: "
   for i in range(10):
      s = rand_restart_hillclimb(domain, schedulecost)
      cost = schedulecost(s)
      print cost
   '''
test()