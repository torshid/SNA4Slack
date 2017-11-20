d3.json("path.json", function(error, graph) {
  if (error) throw error;

}).header("Content-Type","application/x-www-form-urlencoded").send("POST", "threshold=" + threshold + "&key=" + key);