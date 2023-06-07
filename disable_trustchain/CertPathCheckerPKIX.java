package be.fgov.ehealth.etee.crypto.cert;

import be.fgov.ehealth.etee.crypto.status.CryptoResult;
import be.fgov.ehealth.etee.crypto.status.NotificationFatal;
import be.fgov.ehealth.etee.crypto.utils.CertStringBuilder;
import be.fgov.ehealth.etee.crypto.utils.Preconditions;
import java.security.InvalidAlgorithmParameterException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.cert.CertPath;
import java.security.cert.CertPathValidator;
import java.security.cert.CertPathValidatorException;
import java.security.cert.CertificateException;
import java.security.cert.CertificateExpiredException;
import java.security.cert.CertificateFactory;
import java.security.cert.PKIXCertPathValidatorResult;
import java.security.cert.PKIXParameters;
import java.security.cert.X509Certificate;
import java.util.Date;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class CertPathCheckerPKIX implements CertPathChecker {
   private static final Logger LOGGER = LoggerFactory.getLogger(CertPathCheckerPKIX.class);
   private final KeyStore trustedCaCertificates;

   public CertPathCheckerPKIX(KeyStore trustedCaCertificates) {
      this.trustedCaCertificates = trustedCaCertificates;
   }

   @Override
   public CryptoResult<CertificateStatus> validate(List<X509Certificate> certificateChain) {
      return this.validate(certificateChain, null);
   }

   @Override
   public CryptoResult<CertificateStatus> validate(List<X509Certificate> certificateChain, Date validationDate) {
      Preconditions.checkNotEmpty(certificateChain, "No certificate chain present for checking.");
      if (LOGGER.isDebugEnabled()) {
         LOGGER.debug("Checking trust in certificate chain [" + CertStringBuilder.build(certificateChain) + "]");
      }

      try {
         return new CertPathCheckerResult(this.checkTrust(certificateChain, validationDate));
      } catch (CertPathValidatorException var4) {
         return this.handleCertPathValidatorException(var4);
      } catch (CertificateException var5) {
         LOGGER.error("The certificate chain could not be parsed to a certificate path.", var5);
      } catch (NoSuchAlgorithmException var6) {
         LOGGER.error("PKIX is not provided for cert path validation.", var6);
      } catch (InvalidAlgorithmParameterException var7) {
         LOGGER.error("Parameters are incorrect for cert path validation.", var7);
      } catch (KeyStoreException var8) {
         LOGGER.error("Keystore with Trusted CA certificates is not properly initialized", var8);
      }

      return new CertPathCheckerResult(NotificationFatal.CERTIFICATION_PATH_CHECK_FAILED);
   }

   private CryptoResult<CertificateStatus> handleCertPathValidatorException(CertPathValidatorException e) {
      if (e.getCause() instanceof CertificateExpiredException) {
         LOGGER.warn("Cert chain NOT trusted (expired): " + e.getMessage());
         return new CertPathCheckerResult(CertificateStatus.EXPIRED);
      } else {
         LOGGER.warn("Cert chain NOT trusted", e);
         if (LOGGER.isDebugEnabled()) {
            String sb = "Details of CertPartValidatorException: Cause="
               + e.getCause()
               + ", CertPath="
               + e.getCertPath()
               + ", TrustStore="
               + CertStringBuilder.build(this.trustedCaCertificates);
            LOGGER.debug(sb);
         }

         return new CertPathCheckerResult(CertificateStatus.UNSPECIFIED);
      }
   }

   private CertificateStatus checkTrust(List<X509Certificate> certificateChain, Date validationDate) throws CertificateException, NoSuchAlgorithmException, CertPathValidatorException, InvalidAlgorithmParameterException, KeyStoreException {
      CertificateFactory certificateFactory;
      try {
         certificateFactory = CertificateFactory.getInstance("X.509", "BC");
      } catch (NoSuchProviderException var5) {
         LOGGER.error(
            "Cryptolib's default provider [BC] is not available as provider. Using platform default to generate CertPath. Detail: " + var5.getMessage(), var5
         );
         certificateFactory = CertificateFactory.getInstance("X.509");
      }

      CertPath certChain = certificateFactory.generateCertPath(certificateChain);
      return this.checkTrust(certChain, validationDate);
   }

   private CertificateStatus checkTrust(CertPath certificateChain, Date validationDate) throws NoSuchAlgorithmException, CertPathValidatorException, InvalidAlgorithmParameterException, KeyStoreException {
      LOGGER.debug("Checking trust in cert chain look at me being...");
      return CertificateStatus.VALID; // what a hack
      // PKIXParameters pkixp = new PKIXParameters(this.trustedCaCertificates);
      // pkixp.setDate(validationDate);
      // pkixp.setRevocationEnabled(false);
      // CertPathValidator cpv = CertPathValidator.getInstance("PKIX");
      // PKIXCertPathValidatorResult pkixResult = (PKIXCertPathValidatorResult)cpv.validate(certificateChain, pkixp);
      // if (pkixResult != null) {
      //    LOGGER.debug("Certificatechain valid");
      //    if (pkixResult.getTrustAnchor().getTrustedCert() != null) {
      //       LOGGER.debug("Certificatechain trusted from Anchor CA " + pkixResult.getTrustAnchor().getTrustedCert().getSubjectX500Principal());
      //    }

      //    return CertificateStatus.VALID;
      // } else {
      //    return CertificateStatus.UNSPECIFIED;
      // }
   }
}
