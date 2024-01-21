const AuthLayout = ({
    children
  }: {
    children: React.ReactNode;
  }) => {
    return ( 
      <main className="h-full bg-[#b4cbe0] flex items-center justify-center">
        {children}
      </main>
    );
  }
   
  export default AuthLayout;