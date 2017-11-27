the steps by which the project works
1) user enters slack token + sna metric + threshold
2) flask retrieves the data needed (users, channels, ...) from slack server
3) flask puts the received data in our data structures (the ones you see in the class diagram)
4) flask builds the graphs using networkx and sna metric algorithms
5) flask exports the graph in the json format
6) the user browser retrieves the json
7) the JS alchemy library is used to draw the graphs with the json
