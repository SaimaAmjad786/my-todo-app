"use client";

import { ReactNode } from "react";
import { Header } from "./Header";

interface RootLayoutProps {
  children: ReactNode;
}

export function RootLayout({ children }: RootLayoutProps) {
  return (
    <>
      <Header />
      {children}
    </>
  );
}
