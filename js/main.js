function load(){
	d3.selectAll(".title")
		.style("height", function(){
			var container = d3.select(this).node().parentNode
			var h = d3.select(container).select(".thumb").node().getBoundingClientRect().height
			return h
		});
	d3.selectAll(".thumb")
		.on("mouseover", function(){
			var container = d3.select(this).node().parentNode
			console.log(this, container)
			d3.select(container).select(".title").transition().style("opacity",1)
		});
	d3.selectAll(".thumb")
		.on("mouseout", function(){
			var container = d3.select(this).node().parentNode
			console.log(this, container)
			d3.select(container).select(".title").transition().style("opacity",0)
		});
	d3.select("#github")
		.on("mouseover", function(){
			d3.select(this).attr("src","img/github_hover.png")
		})
		.on("mouseout", function(){
			d3.select(this).attr("src","img/github.png")
		})
	d3.select("#info")
		.on("mouseover", function(){
			d3.select(this).attr("src","img/info_hover.png")
			d3.select(".tooltip")
				.style("display","block")
		})
		.on("mouseout", function(){
			d3.select(this).attr("src","img/info.png")
			d3.select(".tooltip")
				.style("display","none")
		})
}
$( window ).load(load);		
$( window ).resize(load);
