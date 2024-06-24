import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StyleSheet } from 'react-native';
import { useState } from 'react';
import { ItemProvider } from './context/ItemContext';

import Start from './pages/start';
import PlaceItem from './pages/placeitem';
import AnalyzingProgress from './pages/analyzingprogress';
import ItemAnalyzed from './pages/itemanalyzed';
import CurrentlyUsed from './pages/currentlyused';
import EnterRoom from './pages/enterroom';

const Stack = createStackNavigator();

export default function App() {
  const [item, setItem] = useState<string>('');


  

type RootStackParamList = {
  Start: undefined ;
  FirstScreen: undefined; 
  AnalyzingProgress: undefined;
  PlaceItem: undefined;
  ItemAnalyzed: undefined;
  CurrentlyUsed: undefined;
  EnterRoom: undefined;
  
  // andere Routen hier hinzufügen
};
const Stack = createStackNavigator<RootStackParamList>();

  return (
    <ItemProvider>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="FirstScreen" component={Start} options={{ headerShown: false }} />
          <Stack.Screen name="AnalyzingProgress" component={AnalyzingProgress} options={{ headerShown: false }} />
          <Stack.Screen name="PlaceItem" component={PlaceItem} options={{ headerShown: false }} />
          <Stack.Screen name="ItemAnalyzed" component={ItemAnalyzed} options={{ headerShown: false }} />
          <Stack.Screen name="CurrentlyUsed" component={CurrentlyUsed} options={{ headerShown: false }} />
          <Stack.Screen name="EnterRoom" component={EnterRoom} options={{ headerShown: false }} />
          <Stack.Screen name="Start" component={Start} options={{ headerShown: false }} />
        </Stack.Navigator>
      </NavigationContainer>
    </ItemProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
