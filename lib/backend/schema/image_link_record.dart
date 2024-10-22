import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class ImageLinkRecord extends FirestoreRecord {
  ImageLinkRecord._(
    super.reference,
    super.data,
  ) {
    _initializeFields();
  }

  // "name" field.
  String? _name;
  String get name => _name ?? '';
  bool hasName() => _name != null;

  // "image" field.
  String? _image;
  String get image => _image ?? '';
  bool hasImage() => _image != null;

  void _initializeFields() {
    _name = snapshotData['name'] as String?;
    _image = snapshotData['image'] as String?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('imageLink');

  static Stream<ImageLinkRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => ImageLinkRecord.fromSnapshot(s));

  static Future<ImageLinkRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => ImageLinkRecord.fromSnapshot(s));

  static ImageLinkRecord fromSnapshot(DocumentSnapshot snapshot) =>
      ImageLinkRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static ImageLinkRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      ImageLinkRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'ImageLinkRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is ImageLinkRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createImageLinkRecordData({
  String? name,
  String? image,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'name': name,
      'image': image,
    }.withoutNulls,
  );

  return firestoreData;
}

class ImageLinkRecordDocumentEquality implements Equality<ImageLinkRecord> {
  const ImageLinkRecordDocumentEquality();

  @override
  bool equals(ImageLinkRecord? e1, ImageLinkRecord? e2) {
    return e1?.name == e2?.name && e1?.image == e2?.image;
  }

  @override
  int hash(ImageLinkRecord? e) =>
      const ListEquality().hash([e?.name, e?.image]);

  @override
  bool isValidKey(Object? o) => o is ImageLinkRecord;
}
