import matplotlib.pyplot as plt
import collections
import numpy as np

def main():
	plurality_hotspots_proportionality = collections.OrderedDict([(1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 3.642857142857143), (9, 5.1), (10, 3.642857142857143), (11, 12.142857142857142), (12, 11.9), (13, 6.538461538461538), (14, 4.25), (15, 8.5), (16, 8.5), (17, 16.12), (18, 22.333333333333332), (19, 13.214285714285714), (20, 16.5), (21, 17.0), (22, 17.928571428571427), (23, 23.23076923076923), (24, 26.7), (25, 19.142857142857142), (26, 24.11111111111111), (27, 26.875), (28, 29.470588235294116), (29, 40.888888888888886), (30, 40.0), (31, 36.6), (32, 36.5), (33, 42.27272727272727), (34, 52.42857142857143), (35, 46.15384615384615), (36, 53.666666666666664), (37, 50.0), (38, 37.90909090909091), (39, 51.416666666666664), (40, 52.53846153846154), (41, 50.0), (42, 56.6), (43, 50.0), (44, 63.0), (45, 60.72727272727273), (46, 73.2), (47, 71.18181818181819), (48, 66.77777777777777), (49, 73.0), (50, 70.875), (51, 75.46666666666667), (52, 75.25), (53, 85.11111111111111), (54, 86.18181818181819), (55, 83.125), (56, 88.3), (57, 86.8), (58, 88.66666666666667), (59, 85.375), (60, 88.2), (61, 93.92857142857143), (62, 97.57142857142857), (63, 92.15384615384616), (64, 93.2), (65, 92.15384615384616), (66, 96.22222222222223), (67, 100.0), (68, 91.5), (69, 98.86666666666666), (70, 97.57142857142857), (71, 96.6), (72, 100.0), (73, 100.0), (74, 100.0), (75, 100.0), (76, 100.0), (77, 100.0), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0)])
	plurality_nohotspots_proportionality = collections.OrderedDict([(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 1.7), (14, 0), (15, 2.125), (16, 5.5), (17, 8.25), (18, 13.222222222222221), (19, 6.8), (20, 17.0), (21, 16.666666666666668), (22, 13.11111111111111), (23, 21.0), (24, 25.25), (25, 0.0), (26, 21.428571428571427), (27, 58.5), (28, 22.166666666666668), (29, 33), (30, 25.0), (31, 27.125), (32, 33.333333333333336), (33, 44.333333333333336), (34, 54.25), (35, 57.0), (36, 66.66666666666667), (37, 83.0), (38, 42.0), (39, 75.0), (40, 69.0), (41, 83.0), (42, 80.0), (44, 83.4), (45, 100.0), (46, 83.5), (47, 97.16666666666667), (48, 91.5), (49, 92.71428571428571), (50, 100.0), (51, 100.0), (52, 96.6), (53, 96.6), (54, 95.75), (55, 97.57142857142857), (56, 98.11111111111111), (57, 100.0), (58, 96.6), (59, 100.0), (60, 97.875), (61, 100.0), (62, 100.0), (63, 100.0), (64, 97.16666666666667), (65, 100.0), (66, 100.0), (67, 100.0), (68, 100.0), (69, 100.0), (70, 100.0), (71, 100.0), (72, 100.0), (73, 100.0), (74, 100.0), (75, 100.0), (76, 100.0), (77, 100.0), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	plurality_hotspots_noproportionality = collections.OrderedDict([(1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 2.4285714285714284), (9, 2.125), (10, 10.736842105263158), (11, 14.166666666666666), (12, 15.3), (13, 15.785714285714286), (14, 14.571428571428571), (15, 23.736842105263158), (16, 33.0), (17, 28.2), (18, 31.0), (19, 33.0625), (20, 33.0), (21, 41.5), (22, 42.714285714285715), (23, 50.0), (24, 47.57142857142857), (25, 50.0), (26, 51.416666666666664), (27, 55.666666666666664), (28, 56.8), (29, 61.333333333333336), (30, 61.333333333333336), (31, 65.58333333333333), (32, 63.6), (33, 67.0), (34, 67.0), (35, 68.36363636363636), (36, 69.9090909090909), (37, 71.57142857142857), (38, 72.89473684210526), (39, 83.0), (40, 79.3076923076923), (41, 80.33333333333333), (42, 79.57142857142857), (43, 71.0), (44, 75.61538461538463), (45, 77.66666666666667), (46, 79.8), (47, 83.0), (48, 83.0), (49, 81.0), (50, 87.25), (51, 79.0), (52, 83.0), (53, 84.94444444444444), (54, 80.33333333333333), (55, 88.66666666666667), (56, 84.7), (57, 83.0), (58, 87.85714285714286), (59, 91.5), (60, 90.15789473684211), (61, 87.25), (62, 88.66666666666667), (63, 88.3125), (64, 87.375), (65, 91.5), (66, 91.5), (67, 94.33333333333333), (68, 91.5), (69, 94.9), (70, 96.6), (71, 96.6), (72, 97.57142857142857), (73, 100.0), (74, 98.3), (75, 94.33333333333333), (76, 99.22727272727273), (77, 98.58333333333333), (78, 98.6923076923077), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100)])
	plurality_nohotspots_noproportionality = collections.OrderedDict([(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 6.8), (11, 0.0), (12, 8.5), (13, 9.714285714285714), (14, 0.0), (15, 13.0), (16, 33), (17, 22.22222222222222), (18, 23.4), (19, 29.8), (20, 33.0), (21, 41.5), (22, 38.666666666666664), (23, 43.2), (24, 43.2), (25, 50.0), (26, 45.142857142857146), (28, 62.75), (29, 50), (30, 58.5), (31, 67.0), (32, 58.5), (33, 71.57142857142857), (34, 77.66666666666667), (35, 81.22222222222223), (36, 83), (37, 83.0), (38, 83.0), (39, 83.0), (40, 83.0), (41, 83), (42, 83.2), (43, 83), (44, 83.0), (45, 91.5), (46, 83.0), (47, 83.0), (49, 91.5), (50, 95.75), (51, 90.28571428571429), (52, 93.2), (53, 90.28571428571429), (54, 91.5), (55, 100), (56, 94.33333333333333), (57, 100.0), (58, 100.0), (59, 100.0), (60, 100.0), (61, 96.6), (62, 100.0), (63, 98.11111111111111), (64, 100.0), (65, 100.0), (66, 100.0), (67, 100.0), (68, 100.0), (69, 100.0), (70, 100.0), (71, 100.0), (72, 100.0), (73, 100.0), (74, 100.0), (75, 100.0), (76, 100.0), (77, 100.0), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	borda_hotspots_proportionality  = collections.OrderedDict([(3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 1.7), (13, 0.0), (14, 0.0), (15, 4.25), (16, 7.285714285714286), (17, 10.2), (18, 0.0), (19, 5.666666666666667), (20, 4.857142857142857), (21, 8.5), (22, 11.333333333333334), (23, 4.25), (24, 14.166666666666666), (25, 10.2), (26, 10.625), (27, 9.272727272727273), (28, 5.666666666666667), (29, 12.75), (30, 11.166666666666666), (31, 18.875), (32, 16.857142857142858), (33, 21.9), (34, 24.0), (36, 24.875), (37, 25.0), (38, 25.1), (39, 23.857142857142858), (40, 35.25), (41, 16.75), (42, 30.857142857142858), (43, 30.0), (44, 22.333333333333332), (45, 31.333333333333332), (46, 36.4), (47, 36.18181818181818), (48, 33.142857142857146), (49, 42.44444444444444), (50, 45.75), (51, 52.833333333333336), (52, 35.25), (53, 37.50000000000001), (54, 46.6), (55, 39.8), (56, 50.0), (57, 57.142857142857146), (58, 61.7), (59, 54.857142857142854), (60, 52.833333333333336), (61, 69.58333333333333), (62, 64.28571428571429), (63, 67.0), (64, 66.8), (65, 69.14285714285714), (66, 74.0), (67, 74.27272727272727), (68, 73.4), (69, 73.4), (70, 84.25), (71, 89.375), (72, 81.91666666666667), (73, 89.14285714285714), (74, 94.76923076923077), (75, 93.3), (76, 88.75), (77, 94.05882352941177), (78, 92.27272727272727), (79, 100.0), (80, 96.875), (81, 97.875), (82, 98.58333333333333), (83, 100.0), (84, 100.0), (85, 99.10526315789474), (86, 100.0), (87, 100.0), (88, 99.19047619047619), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0)])
	borda_nohotspots_proportionality  = collections.OrderedDict([(0, 0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (13, 0.0), (14, 0.0), (15, 0.0), (16, 0.0), (17, 0.0), (18, 0.0), (19, 0.0), (20, 0.0), (21, 0.0), (22, 0), (23, 0.0), (24, 0.0), (25, 0.0), (26, 0.0), (27, 0.0), (28, 0.0), (29, 0.0), (30, 0.0), (31, 0.0), (32, 5.666666666666667), (33, 17), (34, 14.428571428571429), (35, 17), (36, 3.4), (37, 0.0), (38, 6.25), (39, 7.555555555555555), (40, 27.666666666666668), (41, 33), (42, 21.571428571428573), (43, 16.625), (44, 23.4), (45, 25.0), (46, 16.666666666666668), (47, 40.57142857142857), (48, 39.0), (49, 41.5), (50, 47.333333333333336), (51, 53.4), (52, 47.166666666666664), (53, 36.6), (54, 53.2), (55, 63.4), (56, 70.33333333333333), (57, 80.0), (58, 86.16666666666667), (59, 77.66666666666667), (60, 87.5), (61, 88.66666666666667), (62, 100.0), (63, 92.85714285714286), (64, 90.28571428571429), (65, 95.36363636363636), (66, 100.0), (67, 94.33333333333333), (68, 97.875), (69, 97.16666666666667), (70, 100.0), (71, 98.11111111111111), (72, 100.0), (73, 100.0), (74, 100.0), (75, 100.0), (76, 100.0), (77, 100.0), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	borda_hotspots_noproportionality = collections.OrderedDict([(1, 0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 3.7777777777777777), (14, 9.714285714285714), (15, 11.333333333333334), (16, 14.571428571428571), (17, 14.571428571428571), (18, 11.333333333333334), (19, 13.6), (20, 13.6), (21, 8.5), (22, 19.5), (23, 20.1), (24, 26.6), (25, 28.2), (26, 31.22222222222222), (27, 23.4), (28, 28.428571428571427), (29, 29.8), (30, 34.888888888888886), (31, 39.8), (32, 43.2), (33, 50.0), (34, 46.90909090909091), (35, 46.333333333333336), (36, 50.0), (37, 50.0), (38, 50.0), (39, 52.42857142857143), (40, 55.1), (41, 62.75), (42, 65.3), (43, 64.16666666666667), (44, 63.6), (45, 62.75), (46, 65.3), (47, 63.6), (48, 70.2), (49, 68.66666666666667), (50, 64.16666666666667), (51, 66.8), (52, 77.55555555555556), (53, 74.11111111111111), (54, 80.71428571428571), (55, 83.0), (56, 70.2), (57, 83.0), (58, 72.72727272727273), (59, 76.14285714285714), (60, 79.0), (61, 78.63636363636364), (62, 79.0), (63, 80.71428571428571), (64, 79.8), (65, 80.17647058823529), (66, 81.0), (67, 80.38888888888889), (68, 85.83333333333333), (69, 85.42857142857143), (70, 84.88888888888889), (71, 84.54545454545455), (72, 83.07142857142857), (73, 80.33333333333333), (74, 87.85714285714286), (75, 95.75), (76, 90.28571428571429), (77, 89.05882352941177), (78, 90.28571428571429), (79, 100.0), (80, 95.0), (81, 95.27777777777777), (82, 98.78571428571429), (83, 97.57142857142857), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0)])
	borda_nohotspots_noproportionality = collections.OrderedDict([(0, 0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0), (15, 0.0), (16, 0.0), (17, 0.0), (18, 0.0), (19, 5.666666666666667), (20, 1.7), (21, 0.0), (22, 3.4), (23, 5.666666666666667), (24, 5.666666666666667), (25, 14.0), (26, 11.333333333333334), (27, 11.7), (28, 16.833333333333332), (29, 4.25), (30, 20.333333333333332), (31, 23.2), (32, 27.666666666666668), (33, 33.333333333333336), (34, 27.0), (35, 50.0), (36, 47.57142857142857), (37, 50), (38, 50.0), (39, 60.2), (40, 50.0), (41, 56.8), (42, 62.75), (43, 62.142857142857146), (44, 65.11111111111111), (45, 63.6), (46, 67.0), (47, 73.4), (48, 73.0), (49, 76.6), (50, 77.66666666666667), (51, 79.0), (52, 83.0), (53, 83.0), (54, 87.25), (55, 83.0), (56, 95.14285714285714), (57, 80.0), (58, 85.83333333333333), (59, 85.83333333333333), (60, 87.25), (61, 87.375), (62, 86.4), (63, 89.8), (64, 95.75), (65, 100.0), (66, 95.75), (67, 95.75), (68, 95.14285714285714), (69, 98.3), (70, 100.0), (71, 100.0), (72, 100.0), (73, 100.0), (74, 98.58333333333333), (75, 98.86666666666666), (76, 100.0), (77, 97.875), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	copeland_hotspots_proportionality  = collections.OrderedDict([(1, 0), (2, 0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0), (15, 4.857142857142857), (16, 7.555555555555555), (17, 6.375), (18, 2.125), (19, 0.0), (20, 3.7777777777777777), (21, 17.0), (22, 9.714285714285714), (23, 7.7272727272727275), (24, 6.8), (25, 2.8333333333333335), (26, 3.7777777777777777), (27, 2.4285714285714284), (28, 4.25), (29, 0), (30, 10.2), (31, 8.5), (32, 11.8), (33, 18.272727272727273), (34, 20.2), (35, 5.666666666666667), (36, 16.875), (37, 23.4), (38, 13.4), (39, 11.857142857142858), (40, 17.0), (41, 19.5), (42, 28.5), (43, 23.714285714285715), (44, 22.22222222222222), (45, 19.142857142857142), (46, 33.0), (47, 27.25), (48, 41.5), (49, 29.25), (50, 42.23076923076923), (51, 37.5), (52, 35.642857142857146), (53, 35.57142857142857), (54, 33.25), (55, 29.8), (56, 47.57142857142857), (57, 42.785714285714285), (58, 44.333333333333336), (59, 66.71428571428571), (60, 64.0), (61, 42.714285714285715), (62, 76.6), (63, 59.333333333333336), (64, 60.72727272727273), (65, 74.3076923076923), (66, 72.875), (67, 76.33333333333334), (68, 73.75), (69, 83.28571428571429), (70, 76.07142857142857), (71, 86.0), (72, 81.13333333333334), (73, 81.44444444444444), (74, 87.72727272727273), (75, 91.5625), (76, 93.2), (77, 92.27272727272727), (78, 97.57142857142857), (79, 94.76923076923077), (80, 98.11111111111111), (81, 92.44444444444444), (82, 97.57142857142857), (83, 98.3), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0)])
	copeland_nohotspots_proportionality  = collections.OrderedDict([(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0), (15, 0.0), (16, 0.0), (17, 0.0), (18, 0.0), (19, 0.0), (20, 0.0), (21, 0.0), (22, 0.0), (23, 0.0), (24, 0.0), (25, 0.0), (26, 0.0), (27, 0.0), (28, 0), (29, 0.0), (30, 0.0), (31, 0.0), (32, 0.0), (33, 0.0), (34, 6.25), (35, 5.666666666666667), (36, 0.0), (37, 5.666666666666667), (38, 11.333333333333334), (39, 11.333333333333334), (40, 5.0), (41, 8.5), (42, 14.0), (43, 12.75), (44, 3.4), (45, 11.333333333333334), (46, 0.0), (47, 33.0), (48, 33.25), (49, 39.0), (50, 35.857142857142854), (51, 50.0), (52, 44.5), (53, 33.333333333333336), (54, 38.666666666666664), (55, 61.0), (56, 66.66666666666667), (57, 53.77777777777778), (58, 73.4), (59, 73.2), (60, 89.9), (61, 83.2), (62, 88.83333333333333), (63, 92.71428571428571), (64, 91.5), (65, 97.16666666666667), (66, 94.0), (67, 92.71428571428571), (68, 100.0), (69, 97.16666666666667), (70, 96.22222222222223), (71, 97.875), (72, 100.0), (73, 100.0), (74, 100.0), (75, 100.0), (76, 96.6), (77, 100.0), (78, 100.0), (79, 100.0), (80, 100.0), (81, 100.0), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	copeland_hotspots_noproportionality = collections.OrderedDict([(2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 2.8333333333333335), (12, 3.4), (13, 4.25), (14, 8.5), (15, 2.4285714285714284), (16, 5.666666666666667), (17, 11.333333333333334), (18, 12.142857142857142), (19, 12.363636363636363), (20, 14.571428571428571), (21, 11.166666666666666), (22, 14.75), (23, 11.333333333333334), (24, 23.4), (25, 22.22222222222222), (26, 9.714285714285714), (27, 28.285714285714285), (28, 29.444444444444443), (29, 33.333333333333336), (30, 22.166666666666668), (31, 34.666666666666664), (32, 37.25), (33, 46.6), (34, 40.90909090909091), (35, 40.0), (36, 46.6), (37, 44.333333333333336), (38, 47.57142857142857), (39, 43.3), (40, 41.75), (41, 42.666666666666664), (42, 56.8), (43, 56.8), (44, 60.2), (45, 47.333333333333336), (46, 53.6), (47, 64.57142857142857), (48, 64.16666666666667), (49, 67.0), (50, 65.58333333333333), (51, 62.142857142857146), (52, 66.73333333333336), (53, 69.5), (54, 72.33333333333333), (55, 64.50000000000001), (56, 72.33333333333333), (57, 76.33333333333334), (58, 77.0), (59, 75.0), (60, 78.2), (61, 74.11111111111111), (62, 67.0), (63, 79.3076923076923), (64, 77.18181818181819), (65, 79.8), (66, 83.0), (67, 78.63636363636364), (68, 81.54545454545455), (69, 79.0), (70, 81.0), (71, 83.1), (72, 83.0), (73, 86.1875), (74, 81.84615384615384), (75, 81.76923076923077), (76, 87.25), (77, 86.4), (78, 89.61111111111111), (79, 88.66666666666667), (80, 93.2), (81, 95.75), (82, 96.22222222222223), (83, 94.6875), (84, 98.58333333333333), (85, 99.15), (86, 97.38461538461539), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0)])
	copeland_nohotspots_noproportionality = collections.OrderedDict([(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0), (15, 0.0), (16, 0.0), (17, 0.0), (18, 0.0), (19, 0.0), (20, 0.0), (21, 0.0), (22, 2.6153846153846154), (23, 1.7), (24, 5.666666666666667), (25, 5.666666666666667), (26, 0.0), (27, 5.666666666666667), (28, 3.4), (29, 16.571428571428573), (30, 8.5), (31, 8.25), (32, 0), (33, 20.0), (34, 30.714285714285715), (35, 33.2), (36, 21.285714285714285), (38, 45.285714285714285), (39, 41.75), (40, 53.4), (41, 52.833333333333336), (42, 50.0), (43, 52.833333333333336), (44, 60.2), (45, 67.0), (46, 50.0), (47, 67.0), (48, 62.75), (50, 73.4), (51, 67.0), (52, 77.66666666666667), (53, 78.42857142857143), (54, 75.0), (55, 77.66666666666667), (56, 78.42857142857143), (57, 75.0), (58, 83.0), (59, 77.66666666666667), (60, 83.0), (61, 83.0), (62, 83.0), (63, 84.54545454545455), (64, 91.5), (65, 87.25), (66, 91.5), (67, 93.2), (68, 96.6), (69, 93.2), (70, 100.0), (71, 100.0), (72, 97.57142857142857), (73, 100.0), (74, 100.0), (75, 100.0), (76, 100.0), (77, 98.6923076923077), (78, 98.45454545454545), (79, 100.0), (80, 100.0), (81, 98.86666666666666), (82, 100.0), (83, 100.0), (84, 100.0), (85, 100.0), (86, 100.0), (87, 100.0), (88, 100.0), (89, 100.0), (90, 100.0), (91, 100.0), (92, 100.0), (93, 100.0), (94, 100.0), (95, 100.0), (96, 100.0), (97, 100.0), (98, 100.0), (99, 100.0), (100, 100.0)])
	
	plt.figure()

	one = plurality_hotspots_noproportionality
	two = borda_hotspots_noproportionality
	three = copeland_hotspots_noproportionality
	
	plt.title('Gerrymandering results with hotspots without proportionality constraint')
	plt.plot(one.keys(), one.values(), 'ro', alpha=0.35)
	plt.plot((one.keys()), np.poly1d(np.polyfit(one.keys(), one.values(), 12))((one.keys())), 'r-', label="plurality")
	
	plt.plot(two.keys(), two.values(), 'bo', alpha=0.35)
	plt.plot((two.keys()), np.poly1d(np.polyfit(two.keys(), two.values(), 12))((two.keys())), 'b-', label="Borda")
	
	plt.plot(three.keys(), three.values(), 'go', alpha=0.35)
	plt.plot((three.keys()), np.poly1d(np.polyfit(three.keys(), three.values(), 12))((three.keys())), 'g-', label="Copeland")



	plt.xlabel('Actual percentage')
	plt.ylabel('Gerrymandered percentage')
	plt.legend(loc="upper left")
	plt.savefig("finalgraphs/allrules.png")

if __name__ == "__main__":
    main()