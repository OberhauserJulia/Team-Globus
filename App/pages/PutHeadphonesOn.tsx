// src/screens/PlaceItem.tsx

import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import { Button } from 'react-native-paper';
import axios from 'axios';
import { NavigationProp } from '@react-navigation/native';
import { useItem } from '../context/ItemContext';
import { useEffect } from 'react';
import StopinstallationButton from '../compontens/StopinstallationButton';


interface PlaceItemProps {
  navigation: NavigationProp<any>;
}

export default function PutHeadphonesOn({ navigation }: PlaceItemProps) {
  const { item, setItem } = useItem();
  const [changeScreen, setChangeScreen] = React.useState(false);


  const handlePress = async () => {
    try {
        navigation.navigate('EnterRoom');
        axios.post(`http://${process.env.IP_ADRESS}:4000/api/itemanalyzed/${item}`);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <View style={styles.container}>
      <StopinstallationButton setScreen={setChangeScreen} />
      <Image 
        source={require('../images/decor7.png')} 
        style={styles.image} 
        resizeMode="contain"
      />
      <View style={styles.box}>
        <View style={styles.group}>
          <View style={styles.overlapGroup}>
            <Text style={styles.reflectYourCycle}>
             Put on the Headphones
            </Text>
          </View>
        </View>
      </View>
      <Button
        mode="contained"
        onPress={handlePress}
        style={styles.button}
        labelStyle={{ color: 'black', fontFamily: '', fontSize: 20, textTransform: 'uppercase',}}
      >
        Headphones on 
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignItems: 'center',
  },
  image: {
    width: '50%',
  },
  box: {
    height: 211,
    width: 289,
  },
  group: {
    position: 'absolute', 
    bottom: '100%', // Position text 50% from the bottom of the image
    height: 211,
    width: 297,
  },
  overlapGroup: {
    height: 211,
    width: 289,
    
  },
  reflectYourCycle: {
    color: '#fff',
    fontFamily: '',
    fontSize: 18,
    letterSpacing: 14.4,
    lineHeight: 57.6,
    textAlign: 'center',
    textTransform: 'uppercase',
    bottom: '15%', 
  },
  button: {
    position: 'absolute',
    bottom: '8%', 
    width: '60%',
    height: 64,
    backgroundColor: '#D7D3DB',
    textAlign: 'center',
    justifyContent: 'center',
  },
});
