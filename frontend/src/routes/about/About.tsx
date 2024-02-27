import Navigation from "../../common/Navigation";

function About() {
  return (
    <>
      <div className="flex flex-col">
        <Navigation />
        <div className='flex flex-col items-center justify-center'>
          <h1 className='text-3xl font-bold'>About Us</h1>
          <p className='text-xl max-w-md'>Wooly Quant is a platform for algorithmic trading. We provide tools for developing, testing, and deploying trading algorithms. Our platform is designed to be accessible to traders of all experience levels, and we offer a variety of tools and resources to help you get started. Whether you're a seasoned trader or just getting started, Wooly Quant has something for you.</p>
        </div>
      </div>
    </>
  );
}

export default About;