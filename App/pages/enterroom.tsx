import { View, Text, Image, StyleSheet, Dimensions } from 'react-native';
import { Button } from 'react-native-paper';
import React, { useEffect } from 'react';


export default function EnterRoom({ navigation }) {

    useEffect(() => {
        const timer = setTimeout(() => {
            navigation.navigate('CurrentlyUsed');
        }, 30000);
        return () => clearTimeout(timer);
    }, [navigation]);

    return (

        <View style={styles.container}>
            <Image 
                source={require('../images/decor5.png')} 
                style={styles.image} 
                resizeMode="contain"
            />
            <View style={styles.box}>
                <View style={styles.group}>
                    <View style={styles.overlapGroup}>
                        <Text style={styles.reflectYourCycle}>
                            Please enter
                            {'\n'}
                            the room now
                            {'\n'}
                            and learn
                            {'\n'}
                            about
                            {'\n'}
                            your cycle
                        </Text>
                    </View>
                </View>
            </View>
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
        width: 320,
    },
    group: {
        position: 'absolute',  
        height: 211,
        width: '100%',
    },
    overlapGroup: {
        height: 211,
        width: '100%',
    },
    reflectYourCycle: {
        position: 'absolute', 
        bottom: '8%', 
        color: '#fff',
        fontFamily: 'Helvetica',
        fontSize: 18,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
        width: '100%',
    }
});