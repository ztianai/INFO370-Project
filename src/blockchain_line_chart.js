//(function() {
    var svg1 = d3.select("#blockchain"),
        //margin = {top: 20, right: 80, bottom: 30, left: 50},
        margin = {top: 0, right: 0, bottom: 0, left: 0},
        width = svg1.attr("width") - margin.left - margin.right,
        height = svg1.attr("height") - margin.top - margin.bottom,
        g = svg1.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
     console.log(svg1);
    var parseTime = d3.timeParse("%Y%m%d");

    var x = d3.scaleTime().range([0, width]),
        y = d3.scaleLinear().range([height, 0]),
        z = d3.scaleOrdinal(d3.schemeCategory10);

    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.temperature); });

    d3.tsv("data/user_trajectories.tsv", type, function(error, data) {
    if (error) throw error;

    var cities = data.columns.slice(1).map(function(id) {
        return {
        id: id,
        values: data.map(function(d) {
            return {date: d.date, temperature: d[id]};
        })
        };
    });

    x.domain(d3.extent(data, function(d) { return d.date; }));

    y.domain([
        d3.min(cities, function(c) { return -2.3; }),//d3.min(c.values, function(d) { return d.temperature; }); }),
        d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.temperature; }); })
    ]);

    //print(d3.min(c.values, function(d) { return d.temperature; });)

    z.domain(cities.map(function(c) { return c.id; }));

    svg1.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg1.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("fill", "#000")
        .text("log10 in-degree centrality");

    var city = svg1.selectAll(".city")
        .data(cities)
        .enter().append("g")
        .attr("class", "city");

    city.append("path")
        .attr("class", "line")
        .attr("d", function(d) { return line(d.values); })
        .style("stroke", function(d) { return z(d.id); });

    city.append("text")
        .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
        .attr("x", 3)
        .attr("dy", "0.35em")
        .style("font", "10px sans-serif")
        .text(function(d) { return d.id; });
    });

    function type(d, _, columns) {
    d.date = parseTime(d.date);
    for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
    return d;
    }

//})();
