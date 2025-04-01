document.getElementById('youtubeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const videoUrl = document.getElementById('videoUrl').value;
    
    fetch('http://127.0.0.1:3333/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${"response.status"}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error("data.error");
        }
        displayResults(data);
        displayPieChart(data.sentiment_counts);
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("results").innerHTML = `<p>Error analyzing comments: ${error.message}</p>`;
    });
});

function displayResults(data) {
    const resultsDiv = document.getElementById("results");
    
    // Display total comment count
    resultsDiv.innerHTML = `<h3>Total Comments: ${data.total_comments}</h3>`;

    // Display comment-wise sentiment analysis
    let commentHtml = "<h4>Sentiment Analysis:</h4><ul>";
    data.predictions.forEach(item => {
        commentHtml += `<li><strong>Comment:</strong> ${item.comment} <br> <strong>Sentiment:</strong> ${item.sentiment}</li>`;
    });
    commentHtml += "</ul>";

    resultsDiv.innerHTML += commentHtml;

}

function displayPieChart(sentimentData) {
    const canvas = document.getElementById("sentimentChart");
    const legendContainer = document.getElementById("legend");

    if (!canvas || !legendContainer) {
        console.error("Error: sentimentChart canvas or legend container not found!");
        return;
    }

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const total = Object.values(sentimentData).reduce((sum, value) => sum + value, 0);
    let startAngle = 0;
    const radius = 80;
    const hoverRadius = 90; // Slight expansion on hover
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Different shades of blue
    const colors = { 
        "Positive": "#3498db", // Light Blue
        "Neutral": "#2980b9",  // Medium Blue
        "Negative": "#1c6ea4"  // Dark Blue
    };

    const hoverColors = { 
        "Positive": "#217dbb",
        "Neutral": "#1b5e8b",
        "Negative": "#154d73"
    };

    const slices = [];

    // Clear previous legend
    legendContainer.innerHTML = "";

    // Draw pie chart and store slice data for interaction
    Object.entries(sentimentData).forEach(([sentiment, value]) => {
        const sliceAngle = (value / total) * 2 * Math.PI;
        const endAngle = startAngle + sliceAngle;

        // Calculate the midpoint angle for label placement
        const midAngle = startAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(midAngle) * (radius + 15);
        const labelY = centerY + Math.sin(midAngle) * (radius + 15);

        slices.push({ sentiment, startAngle, endAngle, value, midAngle, labelX, labelY });

        // Draw Pie Slice
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fillStyle = colors[sentiment] || "#ccc";
        ctx.fill();

        // Draw Label
        ctx.fillStyle = "#fff";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";
        ctx.fillText(value, labelX, labelY);

        startAngle = endAngle;

        // Create legend dynamically
        const legendItem = document.createElement("div");
        legendItem.innerHTML = `<span style="display:inline-block;width:15px;height:15px;background:${colors[sentiment]};margin-right:8px;"></span> ${sentiment}`;
        legendItem.style.color = "#fff";
        legendContainer.appendChild(legendItem);
    });

    // Hover effect: Expand the hovered slice, darken color, and show sentiment count
    canvas.addEventListener("mousemove", (event) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        const dx = mouseX - centerX;
        const dy = mouseY - centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > hoverRadius) {
            resetChart(); // Reset if not on a segment
            return;
        }

        const angle = Math.atan2(dy, dx);
        const normalizedAngle = angle >= 0 ? angle : 2 * Math.PI + angle;

        // Redraw chart with expanded hover effect
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        startAngle = 0;
        let foundHover = false;

        slices.forEach(slice => {
            const isHovered = normalizedAngle >= slice.startAngle && normalizedAngle <= slice.endAngle;
            const currentRadius = isHovered ? hoverRadius : radius;
            const fillColor = isHovered ? hoverColors[slice.sentiment] : colors[slice.sentiment];

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, currentRadius, slice.startAngle, slice.endAngle);
            ctx.closePath();
            ctx.fillStyle = fillColor;
            ctx.fill();

            // Draw Label again
            ctx.fillStyle = "#fff";
            ctx.font = isHovered ? "bold 14px Arial" : "bold 12px Arial";
            ctx.fillText(slice.value, slice.labelX, slice.labelY);

            if (isHovered) {
                canvas.title = `${slice.sentiment}: ${slice.value}`;
                foundHover = true;
            }
        });

        if (!foundHover) resetChart(); // Reset if no match
    });

    function resetChart() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        startAngle = 0;

        slices.forEach(slice => {
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, slice.startAngle, slice.endAngle);
            ctx.closePath();
            ctx.fillStyle = colors[slice.sentiment];
            ctx.fill();

            // Draw Labels again
            ctx.fillStyle = "#fff";
            ctx.font = "bold 12px Arial";
            ctx.fillText(slice.value, slice.labelX, slice.labelY);
        });

        canvas.title = ""; // Remove tooltip
    }

    canvas.addEventListener("mouseleave", () => {
        resetChart();
    });

}