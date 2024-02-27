function Login() {
  return (
    <>
      <div className="flex flex-col p-6 md:py-28 space-y-6 md:space-y-28">
        <h1 className="text-xxl text-center">Login</h1>
        <form className="flex flex-col text-center space-y-2">
          <div className="flex flex-col space-y-4 my-6 py-6">
            <div id="login-input" className="shadow">
              <label htmlFor="username">Username </label>
              <input type="text" id="username" name="username" placeholder="Enter your username..." required />
            </div>
            <div id="password-input" className="shadow">
              <label htmlFor="password">Password </label>
              <input type="text" id="password" name="password" placeholder="Enter your password..." required />
            </div>
            <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Login</button>
          </div>
        </form>
      </div>
    </>
  );
}

export default Login;