(ns recommendations2
   (:use clojure.set))

(def critics
   {"Lisa Rose"
     {"Lady in the Water" 2.5, "Snakes on a Plane" 3.5,
      "Just My Luck" 3.0, "Superman Returns" 3.5,
      "You, Me and Dupree" 2.5, "The Night Listener" 3.0},
    "Gene Seymour"
     {"Lady in the Water" 3.0, "Snakes on a Plane" 3.5, 
      "Just My Luck" 1.5, "Superman Returns" 5.0,
      "The Night Listener" 3.0, "You, Me and Dupree" 3.5}, 
    "Michael Phillips"
     {"Lady in the Water" 2.5, "Snakes on a Plane" 3.0,
      "Superman Returns" 3.5, "The Night Listener" 4.0},
    "Claudia Puig"
     {"Snakes on a Plane" 3.5, "Just My Luck" 3.0,
      "The Night Listener" 4.5, "Superman Returns" 4.0, 
      "You, Me and Dupree" 2.5},
    "Mick LaSalle"
     {"Lady in the Water" 3.0, "Snakes on a Plane" 4.0, 
      "Just My Luck" 2.0, "Superman Returns" 3.0,
      "The Night Listener" 3.0, "You, Me and Dupree" 2.0}, 
    "Jack Matthews"
     {"Lady in the Water" 3.0, "Snakes on a Plane" 4.0,
      "The Night Listener" 3.0, "Superman Returns" 5.0,
      "You, Me and Dupree" 3.5},
    "Toby"
     {"Snakes on a Plane" 4.5, "You, Me and Dupree" 1.0,
      "Superman Returns" 4.0}})

; The following function is a bit messy. Make it more readable.
; Tips
; 1) do you have to convert prefs person1/2 to sets?
(defn sim-distance [prefs person1 person2]
   "Returns a distance-based similarity score for person1 and person2"
   (let [p1-prefs (prefs person1)
         p2-prefs (prefs person2)
         items1 (set (keys p1-prefs))
         items2 (set (keys p2-prefs))
         shared-items (intersection items1 items2)]
      (if-not (empty? shared-items)
         ((comp (partial / 1) inc) (reduce +
            (map (fn [shared-item]
               (Math/pow (- (p1-prefs shared-item) (p2-prefs shared-item)) 2))
               shared-items)))
         0)))