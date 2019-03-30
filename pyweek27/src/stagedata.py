import math

helptext = {
	"stage1": "Drag the shards from the icons on the left into the wedge.",
	"stage2": "Position the shards so that the blue points on the right view are within the design.",
	"stage3": "Red diamonds on the right view must not be within the design.",
	
	"color1": "Red diamonds are excluded from the design when in front of a red shape.",
}


store = {
	"stage1": [("Shard", "#ffffff", 4, 4)],
	"stage2": [
		("Shard", "#ffffff", 3, 1),
		("Shard", "#cccccc", 2, 2),
		("Shard", "#ccccff", 1, 3),
	],
	"stage3": [
		("Shard", "#ffffff", 3, 1),
		("Shard", "#cccccc", 2, 2),
		("Shard", "#ccccff", 1, 2),
	],
	"stage4": [
		("Shard", "#ddffdd", 3, 4),
		("Shard", "#ccffff", 2, 4),
		("Shard", "#ddddff", 1, 4),
	],
	"stage5": [
		("Blade", "#ffffcc", 1, 4),
		("Bar", "#eeeedd", 1, 2),
		("Branch", "#ffffcc", 2, 5),
	],
	"stage6": [
		("Blade", "#ffffcc", 1, 5),
		("Bar", "#eeeedd", 2, 2),
		("Branch", "#ffffcc", 2, 4),
		("Shard", "#ccffff", 2, 3),
	],

	"shape1": [
		("Claw", "#ccffff", 4, 2),
		("Shard", "#ffffff", 4, 1),
	],
	"shape2": [
		("Cusp", "#ddeeff", 4, 1),
		("Cusp", "#ddffff", 2, 2),
	],
	"color1": [
		("Blade", "#ccffff", 4, 1),
		("Shard", "#ffaaaa", 2, 2),
	],
	"color2": [
		("Shard", "#ccffff", 4, 3),
		("Shard", "#ffaaaa", 1, 3),
	],
	"color3": [
		("Blade", "#ccffff", 4, 1),
		("Bar", "#ccffff", 4, 1),
		("Shard", "#ccffff", 4, 1),
		("Blade", "#ffaaaa", 1, 1),
		("Bar", "#ffaaaa", 1, 1),
		("Shard", "#ffaaaa", 1, 1),
	],

}

points = {
	"stage1": [
		[],
		[],
	],
	"stage2": [
		[(x, y, 0) for x in (0.1, 0.5, 0.9) for y in (0.3, 0.6, 0.8)],
		[],
	],
	"stage3": [
		[(0.1, 0.8, 0), (0.3, 0.5, 0), (0.5, 0.8, 0), (0.7, 0.5, 0), (0.9, 0.8, 0)],
		[(0.1, 0.5, 0), (0.3, 0.8, 0), (0.5, 0.5, 0), (0.7, 0.8, 0), (0.9, 0.5, 0)],
	],
	"stage4": [
		[(math.phi * j % 1, 0.3 + 0.6 * j / 12, j) for j in range(12)],
		[],
	],
	"stage5": [
		[(math.phi * j % 1, 0.5 + 0.4 * j / 12, (j * 7) % 12) for j in range(12)],
		[],
	],
	"stage6": [
		[(math.phi * 8 * j % 1, 0.3 + 0.67 * (j * 11 * math.phi % 1), j % 12) for j in range(12)],
		[(math.phi * 8 * j % 1, 0.3 + 0.67 * (j * 11 * math.phi % 1), j % 12) for j in range(12, 18)],
	],

	"shape1": [[(0.688, 0.202, 4), (0.291, 0.445, -5), (0.351, 0.445, 0), (0.328, 0.59, 4), (0.115, 0.607, 1), (0.272, 0.848, -3), (0.161, 0.853, -1), (0.858, 0.794, -5), (0.896, 0.623, 1), (0.718, 0.723, 2), (0.936, 0.744, -3)], [(0.486, 0.161, -1), (0.72, 0.327, 1), (0.297, 0.333, -2), (0.439, 0.507, -6), (0.34, 0.711, 3), (0.068, 0.74, -4), (0.708, 0.854, 4), (0.992, 0.9, -1), (0.668, 0.596, -3)]],
	"shape2": [[(0.454, 0.367, -2), (0.207, 0.317, -1), (0.714, 0.316, 4), (0.317, 0.486, 1), (0.346, 0.521, -3), (0.814, 0.73, -5), (0.224, 0.878, 3), (0.428, 0.699, 1), (0.998, 0.545, -6), (0.534, 0.686, -4), (0.054, 0.906, -2), (0.323, 0.885, -5)], [(0.527, 0.28, -4), (0.017, 0.359, -6), (0.836, 0.366, 1), (0.946, 0.669, 2), (0.046, 0.392, 3), (0.023, 0.525, 0), (0.775, 0.823, 5), (0.858, 0.799, -3), (0.122, 0.783, -1), (0.524, 0.868, 4)]],

	"color1": [[(0.512, 0.943, -1), (0.506, 0.928, 2), (0.477, 0.74, -4), (0.462, 0.618, -3), (0.48, 0.424, 4), (0.598, 0.223, -6), (0.792, 0.058, 1), (0.544, 0.385, -2), (0.634, 0.348, -5), (0.411, 0.571, 1)], [(0.573, 0.694, 4), (0.603, 0.634, 0), (0.634, 0.739, 3), (0.986, 0.441, 2), (0.852, 0.868, -2), (0.46, 0.316, 1), (0.264, 0.249, 5), (0.265, 0.391, -3)]],

	"color2": [[(0.208, 0.058, -2), (0.138, 0.26, -6), (0.316, 0.344, 1), (0.646, 0.407, 2), (0.633, 0.667, -5), (0.79, 0.554, -2), (0.193, 0.778, -4), (0.266, 0.883, 3), (0.272, 0.638, 0)], [(0.479, 0.206, -5), (0.017, 0.353, -1), (0.88, 0.638, 4), (0.462, 0.659, 1), (0.414, 0.783, -2), (0.007, 0.809, 0), (0.796, 0.704, 2), (0.732, 0.335, -4)]],
	
	"color3": [[(0.407, 0.348, -3), (0.415, 0.445, 1), (0.342, 0.909, 4), (0.386, 0.662, -4), (0.588, 0.577, 0), (0.619, 0.567, -2), (0.617, 0.542, 4), (0.727, 0.656, -6), (0.906, 0.823, -3), (0.637, 0.831, 1), (0.104, 0.767, 3)], [(0.263, 0.502, -1), (0.569, 0.486, -5), (0.687, 0.113, -2), (0.79, 0.654, 3), (0.782, 0.84, 4), (0.304, 0.829, -6), (0.287, 0.771, 0), (0.111, 0.701, -1), (0.973, 0.659, -3), (0.129, 0.922, 2)]],

}

nexts = {
	"stage1": "stage2",
	"stage2": "stage3",
	"stage3": "stage4",
	"stage4": "stage5",
	"stage5": "stage6",

	"shape1": "shape2",
	"shape2": "shape3",

	"color1": "color2",
	"color2": "color3",

	"size1": "size2",
	"size2": "size3",

}

story = {
	"stage1": "The Queen of Order ruled the seasons, the tides, and the motions of the stars. Regular patterns were always a sign of her handiwork.\nThe Queen of Chaos ruled the storms, the landscapes, and the creatures. Thanks to her influence, no two days were ever the same.",
	"stage2": "The two Queens of Order and Chaos were bitter adversaries, for neither could see beauty in the workings of the other, and so they maintained an uneasy truce.",
	"stage3": "No one knows why truce between the Queens fell apart one day, but they soon faced one another in battle.\nAt the mountain of ice at the Top of the World, they engaged in fierce combat, each fueled by her devotion to her own point of view.",
	"stage4": "In their rage they destroyed the mountain of ice on which they fought. They might have gone on to destroy the entire world, but something happened.\nThe mountain was pulverized into an infinity of tiny, six-pointed shards of ice that filled the sky.",
	"stage5": "As they gazed into the swirling white mist, each Queen saw herself and also her adversary. For each crystal displayed a perfectly ordered symmetry, yet each one was unique. And somehow they came to know that they could coexist after all.",
	"stage6": "The Queens have ruled the world alongside one another ever since. You and I are charged with creating endless variations of snowflakes to remind the world of the beauty that order and chaos may make when they come together.",
}



"""
Atop the mountain of ice at the Top of the World, the Queen of Order and the Queen of Chaos faced off in fierce combat.
The Queen of Order ruled the seasons, the tides, and the motions of the stars. Regular patterns were always a sign of her handiwork.\nThe Queen of Chaos ruled the storms, the landscapes, and the creatures. Thanks to her influence, no two days were ever the same.
The two Queens of Order and Chaos were bitter adversaries, for neither could see beauty in the workings of the other, and so they maintained an uneasy truce.
No one knows why truce between the Queens fell apart one day, but they soon faced one another in battle.\nAt the mountain of ice at the Top of the World, they engaged in fierce combat, each fueled by her devotion to her own point of view.
In their rage they destroyed the mountain of ice on which they fought. They might have gone on to destroy the entire world, but something happened.\nThe mountain was pulverized into an infinity of tiny, six-pointed shards of ice that filled the sky.
As they gazed into the swirling white mist, each Queen saw herself and also her adversary. For each crystal displayed a perfectly ordered symmetry, yet each one was unique. And somehow they came to know that they could coexist after all.
The Queens have ruled the world alongside one another ever since. You and I are charged with creating endless variations of snowflakes to remind the world of the beauty that order and chaos may make when they work together.
"""




