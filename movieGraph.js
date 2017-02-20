
//create the SVG element
var svg = d3.select("body").append("svg").attr("height", "100%").attr("width", "100%");//.style("background","blue");

//read the csv file
var dataSet = [];
d3.csv("movieDB.csv", function (error, data) {
    if (error) {
        console.log(error);
    }
    else {
        data.forEach(function (d) {
            console.log(d);
            dataSet.push(d);
        });
        
        console.log("Data read successfully");
        console.log(dataSet);
        //dataSet = data;
    }
});

//add data to SVG
svg.selectAll("rect")
    .data(dataSet)
    .enter()
    .append("rect")
    .attr("width", 10)
    .attr("height", 20)
    .attr("x", function (i) { return 60 * i; })
    .attr("y", function (d) { return d; });
    