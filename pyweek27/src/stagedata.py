import math

helptext = {
	"stage1": "Drag the shards from the icons on the left into the wedge.",
	"stage2": "Position the shards so that the blue points on the right view are covered.",
	"stage3": "Red points on the right view must not be covered.",
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
		("Bar", "#ffeedd", 1, 2),
		("Branch", "#ffffcc", 2, 5),
	],
	"stage6": [
		("Blade", "#ffffcc", 1, 5),
		("Bar", "#ffeedd", 2, 2),
		("Branch", "#ffffcc", 2, 4),
		("Shard", "#ccffff", 2, 3),
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
}

nexts = {
	"stage1": "stage2",
	"stage2": "stage3",
	"stage3": "stage4",
	"stage4": "stage5",
	"stage5": "stage6",
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




