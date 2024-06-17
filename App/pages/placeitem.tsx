import react from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import { Button } from 'react-native-paper';

export default function PlaceItem({ navigation }) {
    return (
        <View style={styles.container}>
            <Image 
                source={require('../images/decor2.png')} 
                style={styles.image} 
                resizeMode="contain"
            />
            <View style={styles.box}>
                <View style={styles.group}>
                    <View style={styles.overlapGroup}>
                        <Text style={styles.reflectYourCycle}>
                            Place any
                            {'\n'}
                            item inside
                            {'\n'}
                            the box
                        </Text>
                    </View>
                </View>
            </View>
            <Button
                mode="contained"
                onPress={() => navigation.navigate('AnalyzingProgress')}
                style={styles.button}
                labelStyle={{ color: 'black', fontFamily: 'Helvetica', fontSize: 20, textTransform: 'uppercase',}}
            >
                Item Placed
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
        position: 'absolute', 
        bottom: '38%', // Position text 50% from the bottom of the image
        height: 211,
        width: 297,
    },
    overlapGroup: {
        height: 211,
        width: 289,
    },
    reflectYourCycle: {
        color: '#fff',
        fontFamily: 'Helvetica',
        fontSize: 18,
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