import {Image, Text, StyleSheet } from 'react-native';
import React from 'react';
import { ImageBackground } from 'react-native';
import { Button } from 'react-native-paper';


export default function ItemAnalyzed({ navigation }) {
    return (
            <ImageBackground 
            source={require('../images/decor4.png')} 
            style={styles.container}
        >
            <Text style={styles.reflectYourCycle}>
                Shoe
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
                onPress={() => navigation.navigate('EnterRoom')}
                style={styles.button}
                labelStyle={{ color: 'black', fontFamily: 'Helvetica', fontSize: 20, textTransform: 'uppercase',}}
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
        position: 'absolute',
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