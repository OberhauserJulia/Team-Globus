import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import { Button } from 'react-native-paper';
import { NavigationProp } from '@react-navigation/native'; 

interface ItemAnalyzedProps {
    navigation: NavigationProp<any>;
  }




export default function Start({ navigation } : ItemAnalyzedProps ) {

    return (
        <View style={styles.container}>
            <Image source={require('../images/decor.png')} style={styles.image} />
            <View style={styles.box}>
                <View style={styles.group}>
                    <View style={styles.overlapGroup}>
                        <Text style={styles.reflectYourCycle}>
                            REFLECT
                            {'\n'}
                            YOUR
                            {'\n'}
                            CYCLE
                        </Text>
                    </View>
                </View>
            </View>
            <Button
                mode="contained"
                onPress={() => {
                    navigation.navigate('PlaceItem')
                    console.log('Get Started pressed')
                }}
                style={styles.button}
                labelStyle={{ color: 'black', fontFamily: '', fontSize: 20, textTransform: 'uppercase',}}
            >
                Get Started
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
       width: '100%',
    },
    box: {
        height: 211,
        width: 289,
    },
    group: {
        height: 211,
        position: 'absolute',
        width: 297,
    },
    overlapGroup: {
        height: 211,
        width: 289,
    },
    reflectYourCycle: {
        color: '#fff',
        fontFamily: '',
        fontSize: 40,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
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
