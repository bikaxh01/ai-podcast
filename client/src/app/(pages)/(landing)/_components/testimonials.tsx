import React from "react";
import TestimonialCard from "./testimonialCard";

function TestimonialsSection() {
  const testimonials = [
    {
      name: "Aarav Mehta",
      feedback:
        "This service exceeded my expectations. The user experience is top-notch!",
    },
    {
      name: "Sanya Kapoor",
      feedback:
        "Very intuitive and simple to use. I was able to get started in minutes.",
    },
    {
      name: "Ravi Sharma",
      feedback:
        "Excellent customer support and quick response time. Highly recommended.",
    },
    {
      name: "Priya Desai",
      feedback:
        "The design is beautiful and the features are exactly what I needed.",
    },
    {
      name: "Kabir Malhotra",
      feedback:
        "Reliable and efficient. I use it daily and it never disappoints.",
    },
    {
      name: "Ananya Roy",
      feedback: "Super impressed with the performance and ease of use!",
    },
    {
      name: "Vikram Patel",
      feedback:
        "A very helpful platform that solved a lot of my workflow issues.",
    },
    {
      name: "Meera Joshi",
      feedback:
        "Great value for the price. I've already recommended it to others.",
    },
    
    
  ];

  return (
    <div className="flex flex-col items-center justify-center mt-12 space-y-7 px-4">
      <div className="flex flex-col text-center space-y-5">
        <h3 className="text-blue-400 font-semibold">Testimonials</h3>
        <h1 className="text-4xl text-white">
          Explore use cases from our official collection.
        </h1>
      </div>

      <div className="w-[80%] max-w-6xl">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3">
          {testimonials.map((item) => (
            <TestimonialCard
              key={item.name}
              name={item.name}
              feedback={item.feedback}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default TestimonialsSection;
