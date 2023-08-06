SCRIPT = """
// constants
var wo_width = 800,
    wo_height = 400,
    ball_x = 76,
    ball_y = -28,
    ball_r = 10,
    ball_height = 5,
    wall_x = 720,
    wall_y = wo_height,
    wall_w = 60,
    wall_h = 30,
    wall_color1 = 'brown',
    wall_color2 = 'gray',
    cannon_x = 10,
    cannon_y = 460,
    cannon_w = 40,
    cannon_h = 20;



make_world = function(add_wall) {
	setup();
    load_sound();
    
	//Add a floor
	var floor = Matter.Bodies.rectangle(wo_width/2, wo_height, wo_width, 10, {
        label: 'floor',
		density:5000.0,
		friction: 80,
        restitution: 900,
		isStatic: true, //An immovable object
		render: {
			visible: true
		}
	});
	Matter.World.add(world, floor);

    walls = add_wall();
	
	Matter.Events.on(engine, 'collisionStart', function(event) {
	var pairs = event.pairs;

    if( pairs[0].bodyB.label == 'ball') {
         var bx = pairs[0].bodyB.velocity.x, by = pairs[0].bodyB.velocity.y,
             bv = bx**2+by**2;
         if( bv > 60 ){
         
            if( pairs[0].bodyA.label.startsWith('wall')) {
                var tb = pairs[0].bodyA, ox = tb.bounds.min.x, oy = tb.bounds.min.y,
                    vx = tb.velocity.x*20, vy = tb.velocity.y*20;
                var i = 0;
                for( var x = 0; x < 3; x++ ) {
                    for( var y = 0; y < 3; y++ ) {

                        var wall = make_wall(ox+x*(wall_h/3), oy+y*(wall_h/3),
                                            wall_w/3.5, wall_h/3.5, 300, 's_wall'+i, wall_color1);
                        Matter.World.add(world, wall);
                        walls.push(wall);             
                        i ++;   
                    }
                }
                Matter.World.remove(world, pairs[0].bodyA);
                pairs[0].bodyB.label = 'ball_col'
                if( pairs[0].bodyB.sound_disabled ) {
                    heavy_hit.play();
                }
            } else {
                if( pairs[0].bodyB.sound_disabled ) {
                    light_hit.play();
                }
            }
         } else {
             light_hit.play();
             pairs[0].bodyA.label = 'ball_col'
         }
	 }
	});

	//Start the engine
	Matter.Engine.run(engine);
	Matter.Render.run(render);

};

var load_sound = function() {
    blast = new Howl({
        src: ['https://github.com/shibats/mpb_samples/blob/main/assets/blast.mp3?raw=true'],
        preload: true,
        html5: true
    });

    light_hit = new Howl({
        src: ['https://github.com/shibats/mpb_samples/blob/main/assets/light_hit.mp3?raw=true'],
        preload: true,
        html5: true,
        volume: 0.3
    });
    
    heavy_hit = new Howl({
        src: ['https://github.com/shibats/mpb_samples/blob/main/assets/heavy_hit.mp3?raw=true'],
        preload: true,
        html5: true,
        volume: 0.25
    });

};

var setup = function() {
    //Fetch our canvas
	var canvas = document.getElementById('world');

	//Setup Matter JS
	engine = Matter.Engine.create();
	world = engine.world;
	body = Matter.Body;
	render = Matter.Render.create({
		canvas: canvas,
		engine: engine,
		options: { 
			width: wo_width,
			height: wo_height,
			background: 'transparent',
			wireframes: false,
			showAngleIndicator: false
		}
	});

};


var make_wall = function(x, y, w, h, density, label, color ) {
    var wall = Matter.Bodies.rectangle(x, y, w, h, { 
        label: label,
        density: density,
        friction: 1,
        frictionAir: 0.01,
        restitution: 0.001,
        render: {
            fillStyle: color,
            strokeStyle: 'black',
            lineWidth: 1
        }
    });
    return wall
}

add_wall1 = function() {
    //Add a wall
	var walls = [];
	for(var i=0; i <= 5; i++ ) {
        var wall = make_wall(wall_x, wall_y-i*wall_h, wall_w, wall_h, 800, 'wall'+i, wall_color1);
		Matter.World.add(world, wall);
		walls.push(wall);
	}
    return walls;
};

add_wall2 = function() {
    //Add a wall
	var walls = [];
	for(var i=0; i <= 5; i++ ) {
        var col = wall_color2, label = 'hwall'+i;
        if( i == 1 ) {
            col = wall_color1
            label = 'wall'+i;
        }
        var wall = make_wall(wall_x, wall_y-i*wall_h, wall_w, wall_h, 800, label, col);
		Matter.World.add(world, wall);
		walls.push(wall);
	}
    return walls;
};


var bang = function(powder, with_sound) {
    //Add a ball
    var ball = Matter.Bodies.circle(ball_x, ball_y+wo_height-ball_r-ball_height, ball_r, {
        label: 'ball',
        density:2000.0,
        friction: 0.99,
        frictionAir: 0.0002,
        restitution: 0.0001,
        render: {
            fillStyle: '#222',
            strokeStyle: 'black',
            lineWidth: 1
        }
    });
    var v = powder/10;
    body.setVelocity(ball, {x:v, y:-v});
    ball.sound_disabled = false;

    Matter.World.add(world, ball);
    if( with_sound ) { 
        blast.play();
        ball.sound_disabled = true;
    }

    var r = document.getElementById('button_right'),
        l = document.getElementById('button_left');
    r.disabled = true;
    l.disabled = true;

};
"""

HTML_TEMPLATE = """
<html>
	<head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.17.1/matter.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
		<style>
#cannon {
	background-image: url('https://github.com/shibats/mpb_samples/blob/main/assets/cannon2.png?raw=true');
	background-size: cover;
	width: 80px;
	height: 80px;
	margin-top: -112px;
	margin-left: 8px;
	z-index: -10;
}

.world_outer {
	border: solid 1px gray;
	width: 800px;
}

button {
    font-size: 14pt;
	width: 12em;
}

button.right {
	position: relative;
	top: -380px;
	left: 8em;
}

button.left {
	position: relative;
	top: -380px;
	left: 10em;
	
}
		</style>
    </head>
    <body>
		<div class="world_outer">
        <canvas id="world"></canvas>
		</div>
		<button class="right" onclick="bang(${powder}, true);" id="button_right"><span class="material-icons">volume_up</span>大砲を撃つ(音あり)</button>
		<button class="left" onclick="bang(${powder}, false);" id="button_left"><span class="material-icons">volume_off</span>大砲を撃つ(音なし)</button>
		<div id="cannon"></div>
    </body>
	<script>
        ${SCRIPT}

        make_world(add_wall${stage});
	</script>
</html>
"""
