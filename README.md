# Smooth-Mapping

### Code Execution

We have uploaded 3 maps which are [map1.png](./map1.png), [map2.png](./map2.png), and [map3.png](./map3.png) to show working of our idea. **-m** command line option requires you to pass the file path.

```bash
# Execute the mapping.py file
python3 mapping.py -m map1.png
```

### Inspiration

UCSC's campus is quite hilly and the changes in elevation can be tedious for some people to walk across, especially if they have underlying healthy issues.

### What it does

It looks for the smoothest path from the starting point to the destination with the least changes in elevation based on the topographical map.

### How we built it

We used VS Code to create a Python program. We used the Live Share extension plugin from the VS Code marketplace so multiple people could work in the same IDE on the same Python file at once.

### Challenges we ran into

We ran into challenges with the path sometimes blocking itself in and creating bunches on the way to the end point. Sometimes, instead of the finding the elevation it kept bouncing between two neighboring pixels and couldn't successfully create a path.

### Accomplishments that we're proud of

We were able to make a path that goes from the start point to the end point. We were able to smooth it out so that it had the least changes in elevation as possible.

### What we learned

We learned there are more elevation problems than we thought. It took us a while to get the path to form correctly, but once we did it was quite useful. This was the first hackathon for each of us, and it was a pretty fun and constructive experience.