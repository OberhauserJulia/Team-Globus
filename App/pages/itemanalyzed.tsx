import React from 'react';
import { View, Text, StyleSheet, Image, ImageBackground } from 'react-native';
import { Button } from 'react-native-paper';
import { useItem } from '../context/ItemContext';
import { NavigationProp } from '@react-navigation/native';
import axios from 'axios';

interface ItemAnalyzedProps {
  navigation: NavigationProp<any>;
}

export default function ItemAnalyzed({ navigation }: ItemAnalyzedProps) {
  const { item, setItem } = useItem();

  const handlePress = async () => {
    try {
        navigation.navigate('EnterRoom');
       axios.post<{ data: any }>(`http://192.168.119.191:4000/api/itemanalyzed/${item}`);
      
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <ImageBackground 
      source={require('../images/decor4.png')} 
      style={styles.container}
    >
      <Text style={styles.reflectYourCycle}>
        {item}
        {'\n'}
        analyzed
      </Text>

      <Image 
        source={require('../images/check.png')} 
        style={styles.image} 
        resizeMode="contain"
      />

      <Button
        mode="contained"
        onPress={handlePress}
        style={styles.button}
        labelStyle={{ color: 'black', fontFamily: 'Helvetica', fontSize: 20, textTransform: 'uppercase' }}
      >
        Next Step
      </Button>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: '#000',
    justifyContent: 'center',
  },
  reflectYourCycle: {
    position: 'absolute',
    top: '15%',
    color: '#fff',
    fontFamily: 'Helvetica',
    fontSize: 18,
    letterSpacing: 14.4,
    lineHeight: 57.6,
    textAlign: 'center',
    textTransform: 'uppercase',
  },
  image: {
    width: 100,
    height: 100,
    position: 'absolute',
    top: '40%',
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
