
# **Calculation Rules**

  

## **1. Input Values**

- **T**: Total study time
    
- **P**: Passive knowledge ratio (0–1)
    
- **A**: Active knowledge ratio (0–1)
    
- **F**: Focused study ratio (0–1)
    
- **B**: Broad study ratio (0–1)
    

  

### **Conditions**

- P + A = 1
    
- F + B = 1
    

---

## **2. Passive / Active Time Split**

```
Passive_Time = T × P
Active_Time  = T × A
```

---

## **3. Passive Knowledge Internal Split**

```
Passive_Focused = (T × P) × F
Passive_Broad   = (T × P) × B
```

---

## **4. Active Knowledge Internal Split**

```
Active_Focused = (T × A) × F
Active_Broad   = (T × A) × B
```

---

## **5. Subject Allocation Inside Passive × Focused**

- **S**: Subject study time (S ≤ T)
    

```
Subject_Passive_Focused = min(S, Passive_Focused)
Subject_Passive_Broad   = S − Subject_Passive_Focused
```

---

## **6. Subject Internal Ratio Split (e.g. TOEIC LC / RC)**

- **L**: Sub-part 1 ratio (e.g. LC)
    
- **R**: Sub-part 2 ratio (e.g. RC)
    

  

### **Condition**

- L + R = 1
    

```
Part1_Time = S × L
Part2_Time = S × R
```

---

## **7. Applying Focused / Broad Inside Subject**

```
Part1_Focused = (S × L) × F
Part1_Broad   = (S × L) × B

Part2_Focused = (S × R) × F
Part2_Broad   = (S × R) × B
```

---

## **8. One-Line Master Formula**

```
Time = Total_Time × Knowledge_Ratio × Study_Mode_Ratio × Subject_Ratio
```

---

## **9. Example Values Used**

```
T = 6h
P = 0.8
A = 0.2
F = 0.7
B = 0.3

S (TOEIC) = 4h
L (LC) = 0.7
R (RC) = 0.3
```