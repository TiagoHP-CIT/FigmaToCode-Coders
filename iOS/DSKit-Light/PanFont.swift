//
//  PanFont.swift
//  DSKit
//
//  Created by 800046340 on 27/04/21.
//

import UIKit
import Foundation

public class PanFont: NSObject {
        
    // MARK: Display
    public static let display = font(type: .bold, size: .large)
    
    // MARK: H1
    public static let h1 = font(type: .book, size: .medium)
    public static let h1Highlight = font(type: .bold, size: .medium)

    // MARK: Body
    public static let body = font(type: .book, size: .small)
    public static let bodyHighlight = font(type: .bold, size: .small)
    
    // MARK: Tiny
    public static let tiny = font(type: .book, size: .tiny)
    public static let tinyHighlight = font(type: .bold, size: .tiny)
    
    // MARK: Caption
    public static let caption = font(type: .book, size: .caption)
    public static let captionHighlight = font(type: .bold, size: .caption)

    public enum FontType: String {
        case book = "CircularXX-Book"
        case bold = "CircularXX-Bold"
    }
    
    public enum FontSize {
        case caption
        case tiny
        case small
        case medium
        case large
        case dsFontSize2xs
        case dsFontSizexs
        case dsFontSizes
        case dsFontSizem
        case dsFontSizel
        case dsFontSizexl
        case dsFontSize2xl
        case custom(size: CGFloat)
        
        public var rawValue: CGFloat {
            switch self {
            case .caption:
                return 12
            case .tiny:
                return 16
            case .small:
                return 18
            case .medium:
                return 24
            case .large:
                return 32
            case .dsFontSize2xs:
                return 12
            case .dsFontSizexs:
                return 14
            case .dsFontSizes:
                return 16
            case .dsFontSizem:
                return 20
            case .dsFontSizel:
                return 24
            case .dsFontSizexl:
                return 28
            case .dsFontSize2xl:
                return 32
            case .custom(let size):
                return size
            }
        }
    }
    
    public enum LineHeight {
        case dsLineHeight2xs
        case dsLineHeightxs
        case dsLineHeights
        case dsLineHeightm
        case dsLineHeightl
        case dsLineHeightxl
        case dsLineHeight2xl
        case custom(lineHeight: CGFloat)
        
        public var rawValue: CGFloat {
            switch self {
            case .dsLineHeight2xs:
                return 12
            case .dsLineHeightxs:
                return 16
            case .dsLineHeights:
                return 20
            case .dsLineHeightm:
                return 24
            case .dsLineHeightl:
                return 28
            case .dsLineHeightxl:
                return 32
            case .dsLineHeight2xl:
                return 36
            case .custom(let lineHeight):
                return lineHeight
            }
        }
    }
    
    public enum LetterSpacing {
        case dsLetterSpacingNormal
        case dsLetterSpacingTight
        case custom(spacing: CGFloat)
        
        public var rawValue: CGFloat {
            switch self {
            case .dsLetterSpacingNormal:
                return 0
            case .dsLetterSpacingTight:
                return -0.02
            case .custom(let spacing):
                return spacing
            }
        }
    }

    public enum StylisticSetIdentifier {
        case set01
        case set02
        case set03
        case set04
        case set05
        case set06
        case set08
        
        public var rawValue: Int {
            switch self {
            case .set01:
                return 2
            case .set02:
                return 4
            case .set03:
                return 6
            case .set05:
                return 10
            case .set06:
                return 12
            default:
                return 16
            }
        }
    }
    
    public static func font(type: FontType, size: FontSize) -> UIFont {
        return UIFont(name: type.rawValue, size: size.rawValue) ?? UIFont()
    }
    
    public static func font(baseFont: UIFont, size: CGFloat = 0, stylisticIdentifier: PanFont.StylisticSetIdentifier) -> UIFont {
        
        let settings: [UIFontDescriptor.FeatureKey: Int] = [
            .featureIdentifier: kStylisticAlternativesType,
            .typeIdentifier: stylisticIdentifier.rawValue
        ]

        let descriptor = baseFont.fontDescriptor.addingAttributes([.featureSettings: [settings]])
        return UIFont(descriptor: descriptor, size: size)
    }
    
    static func loadFontWith(name: String, type: String = "otf") {
        let frameworkBundle = Bundle(for: PanFont.self)
        let pathForResourceString = frameworkBundle.path(forResource: name, ofType: type)
        let fontData = NSData(contentsOfFile: pathForResourceString!)
        let dataProvider = CGDataProvider(data: fontData!)
        let fontRef = CGFont(dataProvider!)
        var errorRef: Unmanaged<CFError>? = nil

        if (CTFontManagerRegisterGraphicsFont(fontRef!, &errorRef) == false) {
            NSLog("Failed to register font - register graphics font failed - this font may have already been registered in the main bundle.")
        }
    }

    public static func loadFonts() {
        loadFontWith(name: FontType.book.rawValue)
        loadFontWith(name: FontType.bold.rawValue)
    }
}
