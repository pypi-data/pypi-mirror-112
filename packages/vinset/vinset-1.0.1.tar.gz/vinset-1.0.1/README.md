# vinset
Video inset function

This toolbox provides a commandline function that will insert a graph (defined in a CSV file) into a video 

# example usage: 

```
vinset -i input_video.mp4 -o output_video.mp4 -c config.json 
```

The configuration file will reference ```data.csv``` which will have format:

```
CurrentTime, Height, Velocity
0, 0.123, 0.566
0.1, 0.146, 0.232
0.2, 0.157, 0.447
0.3, 0.170, 0.677

...

10.4, 2.321, 0.2442
10.5, 2.324, 0.679
```



# configuration file 

Example configuration file 

```
{ 
  "title" : "title of graph",
  
  // define the appearance of the graph                   
    
      
   // This is the pointer to the actual data 
   "series" : [ { "name"  : "displacement",
                 "position" :  { "x" : 100, 
                                "y" : 100,
                            "width" : 500,
                          "height" : 250 },
                // define the appearance of the graph 
                "background" : { "fill":"black", "opacity" : 0.1 },
                // another display_type are "pen" and "page"
                "display_type": "pen",
                "type"  : "file",
                "input" : "data.csv",
                "t"     : "CurrentTime",
                "y"     : "Height",
                "y-limit" : { "type" : "fixed", "limits" : { "lower" : -1, "upper" : +1 } },
                "t-limit" : { "type" : "time",  "width" : 100 }  // 100 seconds all the time }, 
                { "name"  : "velocity", 
                "position" :  { "x" : 100, 
                                "y" : 100,
                            "width" : 500,
                          "height" : 250 },
                // define the appearance of the graph 
                "background" : { "fill":"black", "opacity" : 0.1 },
                // another display_type is "pointer"
                "display_type": "refresh",
                "type"  : "file",
                "input" : "data.csv",
                "t"     : "CurrentTime",
                "y"     : "Velocity",
                "y-limit" : { "type" : "fixed", "limits" : { "lower" : -1, "upper" : +1 } },
                "t-limit" : { "type" : "time",  "width" : 100 }   // 100 seconds all the time }],
    "pointer_value": {"Enabled": False, "Color": (0,0,255), "Radius": 3}

    
}
``
