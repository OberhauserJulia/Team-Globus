// src/context/ItemContext.tsx

import React, { createContext, useState, useContext, ReactNode } from 'react';

interface ItemContextProps {
  item: string;
  setItem: (item: string) => void;
}

const ItemContext = createContext<ItemContextProps | undefined>(undefined);

export const ItemProvider = ({ children }: { children: ReactNode }) => {
  const [item, setItem] = useState<string>('');

  return (
    <ItemContext.Provider value={{ item, setItem }}>
      {children}
    </ItemContext.Provider>
  );
};

export const useItem = (): ItemContextProps => {
  const context = useContext(ItemContext);
  if (!context) {
    throw new Error('useItem must be used within an ItemProvider');
  }
  return context;
};
