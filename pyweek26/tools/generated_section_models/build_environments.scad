// build_environments.scad: modules to build level sections
//

module pool(diameter=10.0, wall_height=2.0, step_width=3.0, connections=[])
{
    difference() {
        union() {
        difference() {
            cylinder(h=0.5,r1=diameter+step_width,r2=diameter+step_width,$fn=48);
            translate([0,0,-0.1])
                cylinder(h=0.7,r1=diameter,r2=diameter,$fn=48);
        }
        difference() {
            cylinder(h=wall_height,r1=diameter+step_width+1.0,r2=diameter+step_width+1.0,$fn=48);
            translate([0,0,-0.1])
                cylinder(h=wall_height+0.2,r1=diameter+step_width,r2=diameter+step_width,$fn=48);
        }
        }
    
        for (c = connections)
        {
            rotate([0,90,0]) {
                angle = atan2(c[1],c[0]);
                rotate([-angle,0,0]) {
                    cylinder(h=diameter+5.0,r1=c[2],r2=c[2],$fn=48);
                }
            }
        }
    }
}

module straight(length=10.0, width=2.0, dy1=0.0, dy2=0.0, dz=0.0)
{
    dims = [0, 0, 0, 0, 0, (dz/length)];
    matrix = [
        [ 1, dims[0], dims[1], 0 ],
        [ dims[2], 1, dims[4], 0 ],
        [ dims[5], dims[3], 1, 0 ],
        [ 0, 0, 0, 1 ]
    ];
    multmatrix(matrix)
    difference() {
        translate([dy1,0,0])
        union() {
            rotate([0,90,0]) {
                difference() {
                    cylinder(h=(length-dy1-dy2),r1=width+1.0,r2=width+1.0,$fn=24);
                    translate([0,0,-0.1])
                        cylinder(h=(length-dy1-dy2+0.2),r1=width,r2=width,$fn=24);
                }
                difference() {
                    cylinder(h=1.0,r1=width+2.0,r2=width+2.0,$fn=24);
                    translate([0,0,-0.1])
                        cylinder(h=1.2,r1=width,r2=width,$fn=24);
                }
                translate([0,0,(length-dy1-dy2)-1.0]) {
                    difference() {
                        cylinder(h=1.0,r1=width+2.0,r2=width+2.0,$fn=24);
                        translate([0,0,-0.1])
                            cylinder(h=1.2,r1=width,r2=width,$fn=24);
                    }
                }
            }
        }
        translate([0,0,-(2*width+4.0)/2])
            cube([3*length,3*length,2*width+4.0],center=true);
    }
}

module curve(p0=[0,0], center=[0,0], dir=1, angle=0.0, width=2.0)
{
    radius = sqrt((p0[0]-center[0])*(p0[0]-center[0]) + (p0[1]-center[1])*(p0[1]-center[1]));
    if (dir == 0) {
        difference() {
            rotate([0,0,-90])
            difference() {
                rotate_extrude(angle = angle, convexity = 10, $fn=32)
                    translate([radius, 0, 0])
                        circle(r = width+1.0,$fn=24);
                rotate([0,0,-1.0])
                    rotate_extrude(angle = angle+2.0, convexity = 10, $fn=32)
                        translate([radius, 0, 0])
                            circle(r = width,$fn=24);
            }
            translate([0,0,-(2*width+4.0)/2])
                cube([5*radius,5*radius,2*width+4.0],center=true);
        }
    }
    else {
        difference() {
            rotate([0,0,90])
            difference() {
                rotate_extrude(angle = -angle, convexity = 10, $fn=32)
                    translate([radius, 0, 0])
                        circle(r = width+1.0,$fn=24);
                rotate([0,0,1.0])
                    rotate_extrude(angle = -angle-2.0, convexity = 10, $fn=32)
                        translate([radius, 0, 0])
                            circle(r = width,$fn=24);
            }
            translate([0,0,-(2*width+4.0)/2])
                cube([5*radius,5*radius,2*width+4.0],center=true);
        }
    }

}

// test pool
//pool(diameter=12.0000, wall_height=3.0000, step_width=3.0000, connections=[[0.0000,-26.0000,2.0000], [23.6074,0.0000,2.0000]]);

// test straight, slope
//straight(length=26.0000, width=2.0000, dy1=11.8322, dy2=6.7082, dz=0.0000);
//straight(length=29.1549, width=12.0000, dy1=0.0000, dy2=0.0000, dz=-15.0000);

// test curve
//curve(p0=[23.6074, 0.0000], center=[23.6074, 5.0000], dir=0, angle=60.1011, width=2.0000);
//curve(p0=[33.6426, 12.4219], center=[37.9771, 9.9295], dir=1, angle=120.4627, width=2.0000);




