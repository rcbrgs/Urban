model tutorial_gis_city_traffic

global {
	file<geometry> osmfile;
	geometry shape <- envelope(osmfile);
	float step <- 1 #mn;
	date starting_date <- date("2009-12-31") add_hours 4;
	date ending_date <- date("2010-02-01") add_hours 23;
	int nb_people <- 20000;
	int min_work_start <- 5;
	int max_work_start <- 9;
	int min_work_end <- 16; 
	int max_work_end <- 20; 
	float min_speed <- 1 #km / #h;
	float max_speed <- 10 #km / #h; 
	float destroy <- 0.02;
	int repair_time <- 2 ;
	graph the_graph;
	float total_road_length <- 50000;
	
	init {
		create reportAgent;
		//possibility to load all of the attibutes of the OSM data: for an exhaustive list, see: http://wiki.openstreetmap.org/wiki/Map_Features
		create osm_agent from: osmfile with: [highway_str::string(read("highway")), building_str::string(read("building")), osmId::string(read("name"))];

		//from the created generic agents, creation of the selected agents
		ask osm_agent
		{
			if (length(shape.points) = 1 and highway_str != nil)
			{
				create node_agent with: [shape::shape, type:: highway_str];
			} else
			{
				if (highway_str != nil)
				{
					if osmId = "Avenida Mercúrio" {
					   create road with: [shape::shape, type:: highway_str, color:: #black, name:: "Avenida Mercúrio", parentOSMAgent:: osm_agent];
					   } else {
					   create road with: [shape::shape, type:: highway_str, parentOSMAgent:: osm_agent];
					   }
				} else if (building_str != nil)
				{	
					if (building_str = "industrial") {
						create building with: [shape::shape] {
							color <- #blue ;
							type <- "Industrial" ;
						}
					} else if (building_str = "residential") {
						create building with: [shape::shape] {
							color <- #yellow ;
							type <- "Residential" ;
						}
					} else {
						int rndBld <- rnd(9) ;
						if (rndBld = 0) {
							create building with: [shape::shape] {
								color <- #navy ;
								type <- "Industrial" ;
								}
							} else {
								create building with: [shape::shape] {
								color <- #orange ;
								type <- "Residential" ;								
							}
						}
					}					
				}
			}
			total_road_length <- sum(road collect each.road_length);
			//do the generic agent die
			do die;
		}
		
		list<building> residential_buildings <- building where (each.type="Residential");
		list<building> industrial_buildings <- building  where (each.type="Industrial") ;
		create people number: nb_people {
			speed <- rnd(min_speed, max_speed);
			start_work <- rnd (min_work_start, max_work_start);
			end_work <- rnd(min_work_end, max_work_end);
			living_place <- one_of(residential_buildings) ;
			working_place <- one_of(industrial_buildings) ;
			objective <- "resting";
			location <- any_location_in (living_place); 
		}
		map<road,float> weights_map <- road as_map (each:: (each.destruction_coeff * each.shape.perimeter));
		the_graph <- as_edge_graph(road) with_weights weights_map;
	}
	
	reflex update_graph{
		map<road,float> weights_map <- road as_map (each:: (each.destruction_coeff * each.shape.perimeter));
		the_graph <- the_graph with_weights weights_map;
	}
	
	reflex repair_road when: every(repair_time #hour ) {
		road the_road_to_repair <- road with_max_of (each.destruction_coeff) ;
		ask the_road_to_repair {
			destruction_coeff <- 1.0 ;
		}
	}

	reflex updateCSV {
	       if (current_date.minute = 30) {
		  ask reportAgent {
		      string outputString <- string(current_date) + "; " + string(sum(people count(each.the_target != nil))) + "; " + agentsAvMercurio;
		      save (outputString) to: "/home/re/output.csv" format: "text" rewrite: false;
		      		  }
		  ask reportAgent { do resetAvMercurio; }
		  }
	       if (current_date.minute = 0) {
		  ask reportAgent {
      		      string outputString <- string(current_date) + "; " + string(sum(people count(each.the_target != nil))) + "; " + agentsAvMercurio;
		      save (outputString) to: "/home/re/output.csv" format: "text" rewrite: false;
		      	    	  }
  		  ask reportAgent { do resetAvMercurio; }
		  }
		
	}

	reflex checkEnding {
	       if current_date > ending_date {
	       	  do die;
		  }
		  }

	reflex printHeader
	{
	       if current_date = starting_date {
	       	  write "total_road_length: " + total_road_length;
		  }
	}

}

species building {
	string type; 
	rgb color <- #gray  ;
	
	aspect base {
		draw shape color: color ;
	}
}

species road  {
	float destruction_coeff <- rnd(1.0,2.0) max: 2.0;
	int colorValue <- int(255*(destruction_coeff - 1)) update: int(255*(destruction_coeff - 1));
	rgb color <- rgb(min([255, colorValue]),max ([0, 255 - colorValue]),0)  update: rgb(min([255, colorValue]),max ([0, 255 - colorValue]),0) ;
	string name;
	float road_length <- shape.perimeter;
	int peoplePassed;
	osm_agent parentOSMAgent;

	aspect base {
		draw shape color: color ;
	}

	aspect interesting {
	       draw shape color: #red ;
	       }
	
	string type;
	aspect default {
		draw shape color: color ;
	}

	action addPeople(int nPeople) {
	       peoplePassed <- peoplePassed + 1;
	       }
}

species people skills:[moving] {
	rgb color <- #yellow ;
	building living_place <- nil ;
	building working_place <- nil ;
	int start_work ;
	int end_work  ;
	string objective ; 
	point the_target <- nil ;
	string currentRoad;

	reflex time_to_work when: current_date.hour = start_work and objective = "resting"{
		objective <- "working" ;
		the_target <- any_location_in (working_place);
	}
		
	reflex time_to_go_home when: current_date.hour = end_work and objective = "working"{
		objective <- "resting" ;
		the_target <- any_location_in (living_place); 
	} 
	 
	reflex move when: the_target != nil {
		path path_followed <- goto(target:the_target, on:the_graph, return_path: true);
		list<geometry> segments <- path_followed.segments;
		loop line over: segments {
			float dist <- line.perimeter;
			ask road(path_followed agent_from_geometry line) { 
				destruction_coeff <- destruction_coeff + (destroy * dist / shape.perimeter);
				if name = "Avenida Mercúrio" {
				   do addPeople(1);
				   //ask parentOSMAgent { do addAgentAvMercurio; }
				   ask reportAgent { do addAgent; }
				   }
			}
		}
		if the_target = location {
			the_target <- nil ;
		}
	}
	
	aspect base {
		draw circle(4) color: color border: #black;
	}
}

species osm_agent
{
	string highway_str;
	string building_str;
	string osmId;
	int agentsAvMercurio <- 0;

	action addAgentAvMercurio {
	       agentsAvMercurio <- agentsAvMercurio + 1; }
}

species node_agent
{
	string type;
	aspect default
	{
		draw square(3) color: # red;
	}

}

species reportAgent
{
	int agentsAvMercurio <- 0;
	action addAgent
	{
		agentsAvMercurio <- agentsAvMercurio + 1;
	}

	action resetAvMercurio
	{
		agentsAvMercurio <- 0;
	} // action resetAvMercurio
	
} // species reportAgent

experiment road_traffic type: gui {
	parameter "File:" var: osmfile <- file<geometry> (osm_file("/home/re/2025/doutorado/MAC6931 Estudos Avançados em Sistemas de Software/20250423_AvMercurio.osm"));
	parameter "Number of people agents" var: nb_people category: "People" ;
	parameter "Earliest hour to start work" var: min_work_start category: "People" min: 2 max: 8;
	parameter "Latest hour to start work" var: max_work_start category: "People" min: 8 max: 12;
	parameter "Earliest hour to end work" var: min_work_end category: "People" min: 12 max: 16;
	parameter "Latest hour to end work" var: max_work_end category: "People" min: 16 max: 23;
	parameter "minimal speed" var: min_speed category: "People" min: 1 #km/#h ;
	parameter "maximal speed" var: max_speed category: "People" max: 10 #km/#h;
	parameter "Value of destruction when a people agent takes a road" var: destroy category: "Road" ;
	parameter "Number of hours between two road repairs" var: repair_time category: "Road" ;
	
	output {
		display city_display type:3d {
			species building aspect: base ;
			species road aspect: base ;
			species people aspect: base ;
		}
		display chart_display refresh: every(10#cycles)  type: 2d { 
			chart "Raw" type: series size: {1, 0.5} position: {0, 0} {
				data "Agents moving" value: sum(people count(each.the_target != nil)) color: #red ;
			}
		}
	}
}