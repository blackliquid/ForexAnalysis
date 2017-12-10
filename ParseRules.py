import re
import pandas as pd

text = r'''1. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 6314 ==> [EUR_JPY_binarized=1]: 6210   <conf:(0.98)> lift:(3.34) lev:(0.01) conv:(42.42) 
 2. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 17723 ==> [EUR_JPY_binarized=1]: 17413   <conf:(0.98)> lift:(3.34) lev:(0.02) conv:(40.2) 
 3. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 11118 ==> [EUR_JPY_binarized=1]: 10912   <conf:(0.98)> lift:(3.33) lev:(0.01) conv:(37.89) 
 4. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 11937 ==> [EUR_JPY_binarized=1]: 11671   <conf:(0.98)> lift:(3.32) lev:(0.01) conv:(31.54) 
 5. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1]: 14812 ==> [EUR_JPY_binarized=1]: 14455   <conf:(0.98)> lift:(3.31) lev:(0.02) conv:(29.19) 
 6. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_CHF_binarized=1]: 29373 ==> [EUR_JPY_binarized=1]: 28646   <conf:(0.98)> lift:(3.31) lev:(0.04) conv:(28.46) 
 7. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 6703 ==> [EUR_JPY_binarized=1]: 6531   <conf:(0.97)> lift:(3.31) lev:(0.01) conv:(27.33) 
 8. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 9309 ==> [EUR_JPY_binarized=1]: 9069   <conf:(0.97)> lift:(3.31) lev:(0.01) conv:(27.25) 
 9. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_USD_binarized=1]: 26139 ==> [EUR_JPY_binarized=1]: 25455   <conf:(0.97)> lift:(3.31) lev:(0.03) conv:(26.92) 
10. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_USD_binarized=1]: 15897 ==> [EUR_JPY_binarized=1]: 15479   <conf:(0.97)> lift:(3.31) lev:(0.02) conv:(26.76) 
11. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1]: 13005 ==> [EUR_JPY_binarized=1]: 12586   <conf:(0.97)> lift:(3.29) lev:(0.02) conv:(21.84) 
12. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1]: 19521 ==> [EUR_JPY_binarized=1]: 18792   <conf:(0.96)> lift:(3.27) lev:(0.02) conv:(18.86) 
13. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1]: 21484 ==> [EUR_JPY_binarized=1]: 20658   <conf:(0.96)> lift:(3.26) lev:(0.03) conv:(18.33) 
14. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1]: 9282 ==> [EUR_JPY_binarized=1]: 8921   <conf:(0.96)> lift:(3.26) lev:(0.01) conv:(18.09) 
15. [EUR_GBP_binarized=1, GBP_JPY_binarized=1]: 46714 ==> [EUR_JPY_binarized=1]: 44843   <conf:(0.96)> lift:(3.26) lev:(0.06) conv:(17.6) 
16. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1]: 6620 ==> [EUR_JPY_binarized=1]: 6351   <conf:(0.96)> lift:(3.26) lev:(0.01) conv:(17.3) 
17. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1]: 17169 ==> [EUR_JPY_binarized=1]: 16385   <conf:(0.95)> lift:(3.24) lev:(0.02) conv:(15.43) 
18. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1]: 11249 ==> [GBP_JPY_binarized=1]: 10715   <conf:(0.95)> lift:(3.22) lev:(0.01) conv:(14.8) 
19. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 7946 ==> [GBP_JPY_binarized=1]: 7500   <conf:(0.94)> lift:(3.19) lev:(0.01) conv:(12.51) 
20. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1]: 25168 ==> [GBP_JPY_binarized=1]: 23621   <conf:(0.94)> lift:(3.17) lev:(0.03) conv:(11.44) 
21. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1]: 18575 ==> [GBP_JPY_binarized=1]: 17293   <conf:(0.93)> lift:(3.14) lev:(0.02) conv:(10.19) 
22. [EUR_GBP_binarized=1, EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 9800 ==> [EUR_CHF_binarized=1]: 9070   <conf:(0.93)> lift:(3.42) lev:(0.01) conv:(9.78) 
23. [GBP_JPY_binarized=1, EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 7620 ==> [EUR_CHF_binarized=1]: 6999   <conf:(0.92)> lift:(3.39) lev:(0.01) conv:(8.93) 
24. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 8509 ==> [EUR_CHF_binarized=1]: 7774   <conf:(0.91)> lift:(3.37) lev:(0.01) conv:(8.43) 
25. [EUR_GBP_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 6350 ==> [EUR_CHF_binarized=1]: 5788   <conf:(0.91)> lift:(3.37) lev:(0.01) conv:(8.22) 
26. [EUR_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 6890 ==> [EUR_CHF_binarized=1]: 6271   <conf:(0.91)> lift:(3.36) lev:(0.01) conv:(8.1) 
27. [EUR_GBP_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 14369 ==> [EUR_CHF_binarized=1]: 13072   <conf:(0.91)> lift:(3.36) lev:(0.02) conv:(8.07) 
28. [GBP_JPY_binarized=1, EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 11401 ==> [EUR_CHF_binarized=1]: 10319   <conf:(0.91)> lift:(3.34) lev:(0.01) conv:(7.68) 
29. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 9267 ==> [EUR_CHF_binarized=1]: 8385   <conf:(0.9)> lift:(3.34) lev:(0.01) conv:(7.65) 
30. [EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 16314 ==> [EUR_CHF_binarized=1]: 14721   <conf:(0.9)> lift:(3.33) lev:(0.02) conv:(7.46) '''

text =  r'''1. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 6314 ==> [EUR_JPY_binarized=1]: 6210   <conf:(0.98)> lift:(3.34) lev:(0.01) conv:(42.42) 
 2. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 17723 ==> [EUR_JPY_binarized=1]: 17413   <conf:(0.98)> lift:(3.34) lev:(0.02) conv:(40.2) 
 3. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 11118 ==> [EUR_JPY_binarized=1]: 10912   <conf:(0.98)> lift:(3.33) lev:(0.01) conv:(37.89) 
 4. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 11937 ==> [EUR_JPY_binarized=1]: 11671   <conf:(0.98)> lift:(3.32) lev:(0.01) conv:(31.54) 
 5. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1]: 14812 ==> [EUR_JPY_binarized=1]: 14455   <conf:(0.98)> lift:(3.31) lev:(0.02) conv:(29.19) 
 6. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_CHF_binarized=1]: 29373 ==> [EUR_JPY_binarized=1]: 28646   <conf:(0.98)> lift:(3.31) lev:(0.04) conv:(28.46) 
 7. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 6703 ==> [EUR_JPY_binarized=1]: 6531   <conf:(0.97)> lift:(3.31) lev:(0.01) conv:(27.33) 
 8. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 9309 ==> [EUR_JPY_binarized=1]: 9069   <conf:(0.97)> lift:(3.31) lev:(0.01) conv:(27.25) 
 9. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, EUR_USD_binarized=1]: 26139 ==> [EUR_JPY_binarized=1]: 25455   <conf:(0.97)> lift:(3.31) lev:(0.03) conv:(26.92) 
10. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_USD_binarized=1]: 15897 ==> [EUR_JPY_binarized=1]: 15479   <conf:(0.97)> lift:(3.31) lev:(0.02) conv:(26.76) 
11. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1]: 13005 ==> [EUR_JPY_binarized=1]: 12586   <conf:(0.97)> lift:(3.29) lev:(0.02) conv:(21.84) 
12. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CAD_binarized=1]: 19521 ==> [EUR_JPY_binarized=1]: 18792   <conf:(0.96)> lift:(3.27) lev:(0.02) conv:(18.86) 
13. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1]: 21484 ==> [EUR_JPY_binarized=1]: 20658   <conf:(0.96)> lift:(3.26) lev:(0.03) conv:(18.33) 
14. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1]: 9282 ==> [EUR_JPY_binarized=1]: 8921   <conf:(0.96)> lift:(3.26) lev:(0.01) conv:(18.09) 
15. [EUR_GBP_binarized=1, GBP_JPY_binarized=1]: 46714 ==> [EUR_JPY_binarized=1]: 44843   <conf:(0.96)> lift:(3.26) lev:(0.06) conv:(17.6) 
16. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1]: 6620 ==> [EUR_JPY_binarized=1]: 6351   <conf:(0.96)> lift:(3.26) lev:(0.01) conv:(17.3) 
17. [EUR_GBP_binarized=1, GBP_JPY_binarized=1, USD_CHF_binarized=1]: 17169 ==> [EUR_JPY_binarized=1]: 16385   <conf:(0.95)> lift:(3.24) lev:(0.02) conv:(15.43) 
18. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1]: 11249 ==> [GBP_JPY_binarized=1]: 10715   <conf:(0.95)> lift:(3.22) lev:(0.01) conv:(14.8) 
19. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 7946 ==> [GBP_JPY_binarized=1]: 7500   <conf:(0.94)> lift:(3.19) lev:(0.01) conv:(12.51) 
20. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1]: 25168 ==> [GBP_JPY_binarized=1]: 23621   <conf:(0.94)> lift:(3.17) lev:(0.03) conv:(11.44) 
21. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1]: 18575 ==> [GBP_JPY_binarized=1]: 17293   <conf:(0.93)> lift:(3.14) lev:(0.02) conv:(10.19) 
22. [EUR_GBP_binarized=1, EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 9800 ==> [EUR_CHF_binarized=1]: 9070   <conf:(0.93)> lift:(3.42) lev:(0.01) conv:(9.78) 
23. [GBP_JPY_binarized=1, EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 7620 ==> [EUR_CHF_binarized=1]: 6999   <conf:(0.92)> lift:(3.39) lev:(0.01) conv:(8.93) 
24. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 8509 ==> [EUR_CHF_binarized=1]: 7774   <conf:(0.91)> lift:(3.37) lev:(0.01) conv:(8.43) 
25. [EUR_GBP_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 6350 ==> [EUR_CHF_binarized=1]: 5788   <conf:(0.91)> lift:(3.37) lev:(0.01) conv:(8.22) 
26. [EUR_JPY_binarized=1, USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 6890 ==> [EUR_CHF_binarized=1]: 6271   <conf:(0.91)> lift:(3.36) lev:(0.01) conv:(8.1) 
27. [EUR_GBP_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 14369 ==> [EUR_CHF_binarized=1]: 13072   <conf:(0.91)> lift:(3.36) lev:(0.02) conv:(8.07) 
28. [GBP_JPY_binarized=1, EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 11401 ==> [EUR_CHF_binarized=1]: 10319   <conf:(0.91)> lift:(3.34) lev:(0.01) conv:(7.68) 
29. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 9267 ==> [EUR_CHF_binarized=1]: 8385   <conf:(0.9)> lift:(3.34) lev:(0.01) conv:(7.65) 
30. [EUR_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 16314 ==> [EUR_CHF_binarized=1]: 14721   <conf:(0.9)> lift:(3.33) lev:(0.02) conv:(7.46) 
31. [GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 12359 ==> [EUR_JPY_binarized=1]: 11133   <conf:(0.9)> lift:(3.06) lev:(0.01) conv:(7.11) 
32. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 7774 ==> [GBP_JPY_binarized=1]: 6999   <conf:(0.9)> lift:(3.04) lev:(0.01) conv:(7.05) 
33. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 8509 ==> [GBP_JPY_binarized=1]: 7620   <conf:(0.9)> lift:(3.02) lev:(0.01) conv:(6.73) 
34. [GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 12719 ==> [EUR_CHF_binarized=1]: 11386   <conf:(0.9)> lift:(3.31) lev:(0.01) conv:(6.95) 
35. [GBP_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 13242 ==> [EUR_CHF_binarized=1]: 11821   <conf:(0.89)> lift:(3.3) lev:(0.01) conv:(6.79) 
36. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1]: 28435 ==> [GBP_JPY_binarized=1]: 25378   <conf:(0.89)> lift:(3.01) lev:(0.03) conv:(6.54) 
37. [GBP_JPY_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 36712 ==> [EUR_JPY_binarized=1]: 32591   <conf:(0.89)> lift:(3.01) lev:(0.04) conv:(6.28) 
38. [USD_CHF_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 10259 ==> [EUR_CHF_binarized=1]: 9099   <conf:(0.89)> lift:(3.28) lev:(0.01) conv:(6.44) 
39. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 16028 ==> [GBP_JPY_binarized=1]: 14157   <conf:(0.88)> lift:(2.98) lev:(0.02) conv:(6.03) 
40. [USD_CHF_binarized=1, EUR_USD_binarized=1]: 24797 ==> [EUR_CHF_binarized=1]: 21839   <conf:(0.88)> lift:(3.25) lev:(0.03) conv:(6.11) 
41. [EUR_GBP_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1]: 6837 ==> [EUR_CHF_binarized=1]: 6021   <conf:(0.88)> lift:(3.25) lev:(0.01) conv:(6.1) 
42. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 9012 ==> [EUR_JPY_binarized=1]: 7878   <conf:(0.87)> lift:(2.97) lev:(0.01) conv:(5.6) 
43. [GBP_JPY_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 11821 ==> [EUR_JPY_binarized=1]: 10319   <conf:(0.87)> lift:(2.96) lev:(0.01) conv:(5.55) 
44. [GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 28935 ==> [EUR_JPY_binarized=1]: 25062   <conf:(0.87)> lift:(2.94) lev:(0.03) conv:(5.27) 
45. [GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 20264 ==> [EUR_JPY_binarized=1]: 17489   <conf:(0.86)> lift:(2.93) lev:(0.02) conv:(5.15) 
46. [EUR_JPY_binarized=1, GBP_USD_binarized=1]: 82167 ==> [GBP_JPY_binarized=1]: 70903   <conf:(0.86)> lift:(2.91) lev:(0.08) conv:(5.13) 
47. [GBP_JPY_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 13242 ==> [EUR_JPY_binarized=1]: 11401   <conf:(0.86)> lift:(2.92) lev:(0.01) conv:(5.07) 
48. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 9235 ==> [GBP_JPY_binarized=1]: 7878   <conf:(0.85)> lift:(2.88) lev:(0.01) conv:(4.79) 
49. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 14524 ==> [GBP_JPY_binarized=1]: 12366   <conf:(0.85)> lift:(2.87) lev:(0.01) conv:(4.73) 
50. [EUR_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1]: 47664 ==> [GBP_JPY_binarized=1]: 40580   <conf:(0.85)> lift:(2.87) lev:(0.05) conv:(4.73) 
51. [GBP_JPY_binarized=1, EUR_USD_binarized=1]: 61453 ==> [EUR_JPY_binarized=1]: 51974   <conf:(0.85)> lift:(2.87) lev:(0.06) conv:(4.57) 
52. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 8385 ==> [EUR_JPY_binarized=1]: 6999   <conf:(0.83)> lift:(2.83) lev:(0.01) conv:(4.26) 
53. [EUR_JPY_binarized=1, GBP_USD_binarized=1, EUR_USD_binarized=1]: 47965 ==> [GBP_JPY_binarized=1]: 39925   <conf:(0.83)> lift:(2.81) lev:(0.05) conv:(4.2) 
54. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CAD_binarized=1, EUR_USD_binarized=1]: 14905 ==> [EUR_JPY_binarized=1]: 12366   <conf:(0.83)> lift:(2.82) lev:(0.01) conv:(4.14) 
55. [EUR_JPY_binarized=1, GBP_USD_binarized=1, EUR_CHF_binarized=1, EUR_USD_binarized=1]: 30209 ==> [GBP_JPY_binarized=1]: 25062   <conf:(0.83)> lift:(2.8) lev:(0.03) conv:(4.13) 
56. [EUR_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 8509 ==> [GBP_JPY_binarized=1, EUR_CHF_binarized=1]: 6999   <conf:(0.82)> lift:(5.81) lev:(0.01) conv:(4.83) 
57. [GBP_JPY_binarized=1, GBP_USD_binarized=1, USD_CHF_binarized=1, EUR_USD_binarized=1]: 9267 ==> [EUR_JPY_binarized=1]: 7620   <conf:(0.82)> lift:(2.79) lev:(0.01) conv:(3.97) 
58. [GBP_JPY_binarized=1, GBP_USD_binarized=1, EUR_USD_binarized=1]: 48746 ==> [EUR_JPY_binarized=1]: 39925   <conf:(0.82)> lift:(2.78) lev:(0.05) conv:(3.9) 
59. [GBP_JPY_binarized=1, EUR_CHF_binarized=1]: 79739 ==> [EUR_JPY_binarized=1]: 64646   <conf:(0.81)> lift:(2.75) lev:(0.07) conv:(3.73) 
60. [GBP_JPY_binarized=1, USD_CAD_binarized=1, EUR_CHF_binarized=1]: 33857 ==> [EUR_JPY_binarized=1]: 27167   <conf:(0.8)> lift:(2.72) lev:(0.03) conv:(3.57) '''

def parse_rules(text):
    lines = re.split(r"\n", text)
    clean_lines = []

    for line in lines:
        clean_lines.append(re.sub(r'binarized', r'-', re.sub(r'\W|[0-9]|confliftlevconv', r'', line)))

    prereq = []
    conseq = []
    for line in clean_lines:
        temp_list = re.split(r"-", line)

        temp_list_clean = []

        for elem in temp_list[0:-1]:
            temp_list_clean.append(elem[:-1])
        prereq.append(temp_list_clean[0:-1])
        conseq.append(temp_list_clean[-1])


    #binarize attributes

    currencies = ["EUR_USD",
    "USD_JPY",
    "GBP_USD",
    "EUR_GBP",
    "USD_CHF",
    "EUR_JPY",
    "EUR_CHF",
    "USD_CAD",
    "AUD_USD",
    "GBP_JPY"]

    #binarize prereq

    prereq_binarized = pd.DataFrame(columns=currencies)
    for rule in prereq:
        onehot = pd.get_dummies(rule, columns= currencies)
        onehot = pd.DataFrame(onehot.sum(0))
        prereq_binarized = pd.concat([prereq_binarized, onehot.transpose()])
    prereq_binarized.reset_index(inplace=True)
    prereq_binarized.drop(columns = "index", inplace=True)
    prereq_binarized.fillna(0, inplace=True)


    #binarize conseq

    conseq_binarized = pd.DataFrame(columns=currencies)
    for rule in conseq:
        onehot = pd.get_dummies(rule, columns=currencies)
        conseq_binarized = pd.concat([conseq_binarized, onehot])
    conseq_binarized.reset_index(inplace=True)
    conseq_binarized.drop(columns="index", inplace=True)
    conseq_binarized.fillna(0, inplace=True)

    #return prereq_df, conseq_df

    return prereq_binarized, conseq_binarized