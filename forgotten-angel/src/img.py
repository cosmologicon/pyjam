from __future__ import division
import pygame, random, math, os.path
import vista, settings

cache = {}


def getfont(fontsize, fontname):
	key = fontsize, fontname
	if key not in cache:
		if fontname is not None:
			fontname = "fonts/%s.ttf" % fontname
		cache[key] = pygame.font.Font(fontname, fontsize)
	return cache[key]

# http://www.pygame.org/wiki/TextWrapping?parent=CookBook
def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    return [w for line in text.splitlines() for w in wrapline(line, font, maxwidth)]

def gettext(text, fontsize, color, bcolor, fontname, anchor = 0.5, linespace = None, maxwidth = None):
	key = text, fontsize, color, bcolor, fontname, anchor, maxwidth
	if key in cache:
		return cache[key]
	if linespace is None:
		linespace = {
			None: 0.8,
			"jockey": 1,
		}.get(fontname, 1)
	font = getfont(fontsize, fontname)
	texts = text.splitlines() if maxwidth is None else wrap_multi_line(text, font, maxwidth)
	img0s = [font.render(text, True, color) for text in texts]
	img1s = [font.render(text, True, bcolor) for text in texts]
	w = max(img0.get_width() for img0 in img0s)
	hline = int(math.ceil(fontsize * linespace))
	h = fontsize + (len(texts) - 1) * hline
	d = int(math.ceil(0.05 * fontsize))
	cache[key] = surf = pygame.Surface((w + 2 * d, h + 2 * d)).convert_alpha()
	ps = [(int((w - img0.get_width()) * anchor), hline * j) for j, img0 in enumerate(img0s)]
	surf.fill((0,0,0,0))
	for (x0, y0), img1 in zip(ps, img1s):
		for dx in (0, d, 2*d):
			for dy in (0, d, 2*d):
				surf.blit(img1, (x0 + dx, y0 + dy))
	for (x0, y0), img0 in zip(ps, img0s):
		surf.blit(img0, (x0 + d, y0 + d))
	return surf

def getrawimg(imgname):
	global font
	filename = "data/%s.png" % imgname
	if os.path.exists(filename):
		return pygame.image.load(filename).convert_alpha()
		r = int(float(imgname[4:]) * settings.imgscale)
		img = pygame.Surface((2*r, 2*r)).convert_alpha()
		img.fill((0,0,0,0))
		for s in range(8):
			R = int(round(r * (1 - 0.04 * s)))
			color = 255, 255, 255, 255 - 30 * (7 - s)
			pygame.draw.circle(img, color, (r, r), R)
	else:
		img = pygame.Surface((40, 40)).convert_alpha()
		r, g, b = [random.randint(100, 200) for _ in range(3)]
		img.fill((r, g, b, 50))
		t = gettext(imgname, 24, (255, 255, 255), (0, 0, 0), None)
		img.blit(t, t.get_rect(center = img.get_rect().center))
	return img


def getimg(imgname, angle = 0, scale = 1.0, alpha = 1.0, bad = False):
	angle = round(angle / 6) % 60 * 6 if angle else 0
	alpha = round(alpha, 1)
	scale = round(scale, 1)
	key = imgname, angle, scale, alpha, bad
	if key not in cache:
		if angle == 0 and scale == 1.0 and alpha == 1.0 and not bad:
			cache[key] = img = getrawimg(imgname)
		elif alpha == 1.0 and not bad:
			img0 = getimg(imgname)
			cache[key] = pygame.transform.rotozoom(img0, angle, scale)
		elif not bad:
			cache[key] = img0 = getimg(imgname, angle, scale).copy()
			alphas = pygame.surfarray.pixels_alpha(img0)
			alphas *= alpha
		else:
			cache[key] = img0 = getimg(imgname, angle, scale, alpha).copy()
			pixels = pygame.surfarray.pixels3d(img0)
			pixels[:,:,1:3] *= 0.1
	return cache[key]

def draw(imgname, screenpos, angle = None, scale = 1.0, alpha = 1.0, bad = False):
	img = getimg(imgname, angle, scale, alpha, bad)
	r = img.get_rect(center = screenpos)
	vista.screen.blit(img, r)

def worlddraw(imgname, worldpos, angle = None, scale = 1.0, alpha = 1.0):
	scale *= vista.scale / settings.imgscale
	draw(imgname, vista.worldtoscreen(worldpos), angle = angle, scale = scale, alpha = alpha)

def drawtext(text, fontsize, color = (255, 255, 255), bcolor = (0, 0, 0), fontname = None, linespace = None, maxwidth = None, **kwargs):
	anchor = 0.5
	if any("left" in kwarg for kwarg in kwargs):
		anchor = 0
	if any("right" in kwarg for kwarg in kwargs):
		anchor = 0
	surf = gettext(text, fontsize, color, bcolor, fontname, anchor, linespace, maxwidth)
	vista.screen.blit(surf, surf.get_rect(**kwargs))

